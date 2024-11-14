import tensorflow as tf
import numpy as np
import locale
from typing import Dict, Any
from project_types import ProjectType, BuildingParameters, BuildingRatios
import project_types

class UnifiedRealEstatePredictor:
    def __init__(self):
        try:
            locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
        except:
            locale.setlocale(locale.LC_ALL, '')
            
        self.location_prices = {
            "حي النرجس": 5700,
            "حي الملقا": 8334,
            "حي الياسمين": 6995,
            "الرياض": 3000,
            "جدة": 2800,
            "الدمام": 2500,
            "مكة": 3500,
            "المدينة": 2600
        }
        
        self.base_costs = {
            ProjectType.SHOPPING_MALL: 3500,
            ProjectType.RESIDENTIAL: 2800,
            ProjectType.COMMERCIAL: 3200,
            ProjectType.MIXED_USE: 3300,
            ProjectType.VILLA: 2600,
            ProjectType.SINGLE_VILLA: 2500,
            ProjectType.RESIDENTIAL_COMPOUND: 2900,
            ProjectType.ADMIN_BUILDING: 3000
        }
        
        self.models = {}
        self.is_trained = {}
        for project_type in ProjectType:
            self.models[project_type] = self._initialize_model()
            self.is_trained[project_type] = False

    def _initialize_model(self):
        model = tf.keras.Sequential([
            tf.keras.layers.Dense(64, activation='relu', input_shape=(6,)),  # Updated input shape
            tf.keras.layers.Dense(32, activation='relu'),
            tf.keras.layers.Dense(16, activation='relu'),
            tf.keras.layers.Dense(4)
        ])
        
        model.compile(
            optimizer='adam',
            loss='mse',
            metrics=['mae']
        )
        return model

    def _generate_training_data(self, project_type, n_samples=1000):
        X = np.zeros((n_samples, 6))  # Updated feature count
        y = np.zeros((n_samples, 4))
        
        base_cost = self.base_costs[project_type]
        
        for i in range(n_samples):
            location_price = np.random.choice(list(self.location_prices.values()))
            land_area = np.random.uniform(100, 50000)
            floors = np.random.randint(1, 11)
            ratios = BuildingRatios.create(floors)
            effective_ratio = (ratios.ground_floor + 
                             (ratios.upper_floors * (floors - 2)) + 
                             ratios.top_floor) / floors
            demand = np.random.uniform(0.8, 1.2)
            competition = np.random.uniform(0.8, 1.2)
            
            X[i] = [location_price, land_area, floors, effective_ratio, demand, competition]
            
            # Calculate target values
            buildable_area = land_area * effective_ratio * floors
            land_cost = location_price * land_area * (1 + np.random.normal(0, 0.1))
            construction_cost = base_cost * buildable_area * (1 + np.random.normal(0, 0.1))
            
            total_cost = land_cost + construction_cost
            sales_multiplier = 1.4 if project_type == ProjectType.SHOPPING_MALL else 1.3
            rental_multiplier = 0.15 if project_type == ProjectType.SHOPPING_MALL else 0.08
            
            sales_revenue = total_cost * sales_multiplier * demand * (2 - competition) * (1 + np.random.normal(0, 0.1))
            rental_revenue = total_cost * rental_multiplier * demand * (1 + np.random.normal(0, 0.1))
            
            y[i] = [land_cost, construction_cost, sales_revenue, rental_revenue]
        
        return X, y
    def train_project_type(self, project_type: ProjectType, epochs: int = 50):
        """Train the model for a specific project type"""
        # Generate training data
        X, y = self._generate_training_data(project_type)
        
        # Calculate and store normalization parameters
        self.models[project_type].X_mean = X.mean(axis=0)
        self.models[project_type].X_std = X.std(axis=0)
        self.models[project_type].y_mean = y.mean(axis=0)
        self.models[project_type].y_std = y.std(axis=0)
        
        # Normalize data
        X_norm = (X - self.models[project_type].X_mean) / self.models[project_type].X_std
        y_norm = (y - self.models[project_type].y_mean) / self.models[project_type].y_std
        
        # Train the model
        history = self.models[project_type].fit(
            X_norm,
            y_norm,
            epochs=epochs,
            batch_size=32,
            validation_split=0.2,
            verbose=0
        )
        
        self.is_trained[project_type] = True
        return history

    def predict(self, project_type: ProjectType, location: str, land_area: float, floors: int, market_conditions: dict) -> dict:
        if not self.is_trained[project_type]:
            self.train_project_type(project_type)
        
        ratios = BuildingRatios.create(floors)
        effective_ratio = (ratios.ground_floor + 
                         (ratios.upper_floors * (floors - 2)) + 
                         ratios.top_floor) / floors
        
        X = np.array([[
            self.location_prices[location],
            land_area,
            floors,
            effective_ratio,
            market_conditions['demand_level'],
            market_conditions['competition_level']
        ]])
        
        X_norm = (X - self.models[project_type].X_mean) / self.models[project_type].X_std
        y_norm = self.models[project_type].predict(X_norm)
        predictions = y_norm * self.models[project_type].y_std + self.models[project_type].y_mean
        
        land_cost, construction_cost, sales_revenue, rental_revenue = predictions[0]
        
        return self._format_results(
            project_type, location, land_area, floors,
            land_cost, construction_cost, sales_revenue, rental_revenue,
            market_conditions, effective_ratio
        )

    # [Rest of the methods remain the same...]

    def _format_results(self, project_type, location, land_area, floors,
                   land_cost, construction_cost, sales_revenue, rental_revenue,
                   market_conditions, effective_ratio):
        """Format the prediction results"""
        total_cost = land_cost + construction_cost
        design_cost = total_cost * 0.03
        licensing_cost = total_cost * 0.02
        management_cost = total_cost * 0.05
        
        def format_currency(amount: float) -> str:
            return f"{amount:,.0f} ريال"
        
        def format_percentage(value: float) -> str:
            return f"{value:.1f}%"

        # Calculate ROI and payback period
        roi = ((sales_revenue / total_cost) - 1) * 100
        payback_period = total_cost / rental_revenue if rental_revenue > 0 else float('inf')
        result = {
            "تقرير_تحليل_الاستثمار": {
                "تفاصيل_المشروع": {
                    "نوع_المشروع": project_type.value,
                    "الموقع": location,
                    "مساحة_الأرض": f"{land_area:,.0f} متر مربع",
                    "عدد_الطوابق": floors,
                    "نسبة_البناء_الفعالة": f"{effective_ratio:.2f}"
                },
                "توقعات_التمويل": {
                    "تكاليف_المشروع": {
                        "تكلفة_الأرض": format_currency(land_cost),
                        "تكلفة_البناء": format_currency(construction_cost),
                        "تكاليف_إضافية": {
                            "التصميم": format_currency(design_cost),
                            "التراخيص": format_currency(licensing_cost),
                            "الإدارة": format_currency(management_cost)
                        },
                        "التكاليف_الإجمالية": format_currency(total_cost)
                    },
                    "الإيرادات_المتوقعة": {
                        "إيرادات_البيع": format_currency(sales_revenue),
                        "إيرادات_التأجير_السنوية": format_currency(rental_revenue),
                        "العائد_السنوي_المتوقع": format_percentage(rental_revenue / total_cost * 100)
                    }
                },
                "تحليل_السوق": {
                    "مستوى_الطلب": "مرتفع" if market_conditions['demand_level'] > 1 else "متوسط",
                    "مستوى_المنافسة": "منخفض" if market_conditions['competition_level'] < 1 else "متوسط",
                    "نمو_السوق": "مستقر",
                    "توقعات_مستقبلية": self._get_market_outlook(market_conditions['demand_level'], 
                                                               market_conditions['competition_level'])
                },
                "مؤشرات_الأداء": {
                    "العائد_على_الاستثمار": format_percentage(roi),
                    "فترة_الاسترداد": f"{payback_period:.1f} سنة",
                    "معدل_النمو_السنوي": "8-12%",
                    "مستوى_المخاطرة": self._calculate_risk_level(roi, payback_period)
                }
            }
        }
        
    # Add project-specific details
        if project_type == ProjectType.SHOPPING_MALL:  # Changed project_types to project_type
            result["تقرير_تحليل_الاستثمار"]["تفاصيل_إضافية"] = {
                "عدد_المحلات": int(land_area * floors * 0.7 / 100),
            "مساحة_التأجير": f"{land_area * floors * 0.7:,.0f} متر مربع",
            "مواقف_السيارات": f"{int(land_area * 0.4):,d} موقف",
            "المرافق": ["مصاعد", "سلالم كهربائية", "نظام تكييف مركزي", "نظام أمن ومراقبة"]
        }
    
        return result  # Moved outside the if statement to return for all project types

    def _get_market_outlook(self, demand, competition):
        score = demand * (2 - competition)
        if score > 1.2:
            return "ممتاز"
        elif score > 1:
            return "جيد"
        else:
            return "متوسط"

    def _calculate_risk_level(self, roi, payback_period):
        if roi > 25 and payback_period < 5:
            return "منخفض"
        elif roi > 15 and payback_period < 8:
            return "متوسط"
        else:
            return "مرتفع"
