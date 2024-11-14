from dataclasses import dataclass
from enum import Enum
from typing import Dict, Any
import json
import locale

class ProjectType(Enum):
    SHOPPING_MALL = "مول تجاري"
    RESIDENTIAL = "سكني"
    COMMERCIAL = "تجاري"
    MIXED_USE = "متعدد الاستخدامات"
    VILLA = "فلل سكنية"
    SINGLE_VILLA = "فيلا سكنية مفردة"
    RESIDENTIAL_COMPOUND = "مجمع سكني"
    ADMIN_BUILDING = "مبنى إداري"  # Add this line

@dataclass
class BuildingRatios:
    ground_floor: float
    upper_floors: float
    top_floor: float

    @classmethod
    def create(cls, floors: int):
        if floors > 4:
            return cls(
                ground_floor=0.35,
                upper_floors=0.45,
                top_floor=0.70
            )
        else:
            return cls(
                ground_floor=0.65,
                upper_floors=0.75,
                top_floor=0.70
            )

class CommercialRatios(BuildingRatios):
    pass

# Add to the top of the file with other imports and classes
@dataclass
class VillaBuildingRatios:
    ground_floor: float
    first_floor: float
    top_floor: float

    @classmethod
    def create(cls, floors: int) -> 'VillaBuildingRatios':
        if floors > 4:
            return cls(ground_floor=0.35, first_floor=0.45, top_floor=0.70)
        else:
            return cls(ground_floor=0.65, first_floor=0.75, top_floor=0.70)
@dataclass
class AdminBuildingRatios:
    def __init__(self, floors: int):
        if floors > 4:
            self.ground_floor = 0.35
            self.first_floor = 0.45
            self.top_floor = 0.70
        else:
            self.ground_floor = 0.65
            self.first_floor = 0.75
            self.top_floor = 0.70


@dataclass
class SingleVillaBuildingRatios:
    def __init__(self, floors: int):
        if floors > 4:
            self.ground_floor = 0.35
            self.first_floor = 0.45
            self.top_floor = 0.70
        else:
            self.ground_floor = 0.65
            self.first_floor = 0.75
            self.top_floor = 0.70

@dataclass
class CompoundBuildingRatios:
    def __init__(self, floors: int):
        if floors > 4:
            self.ground_floor = 0.35
            self.first_floor = 0.45
            self.top_floor = 0.70
        else:
            self.ground_floor = 0.65
            self.first_floor = 0.75
            self.top_floor = 0.70


@dataclass
class MixedUseRatios:
    ground_floor: float
    first_floor: float
    repeated_floors: float
    top_floor: float

    @classmethod
    def create(cls, floors: int):
        if floors > 4:
            return cls(
                ground_floor=0.35,
                first_floor=0.45,
                repeated_floors=0.45,
                top_floor=0.70
            )
        else:
            return cls(
                ground_floor=0.65,
                first_floor=0.75,
                repeated_floors=0.75,
                top_floor=0.70
            )

class UnifiedCalculator:
    def __init__(self):
        try:
            locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
        except:
            locale.setlocale(locale.LC_ALL, '')
            
        self.location_prices = {
            "حي النرجس": 5700,
            "حي الملقا": 8334,
            "حي الياسمين": 6995
        }

    def format_number(self, number: float) -> str:
        return f"{number:,.0f}"
    def calculate_mall_context(self, land_area: float, location: str, floors: int) -> dict:
        # Initialize building ratios
        ratios = CommercialRatios.create(floors)
        
        # Calculate areas
        ground_floor_area = land_area * ratios.ground_floor
        upper_floor_area = land_area * ratios.upper_floors
        top_floor_area = upper_floor_area * ratios.top_floor
        repeated_floors_total_area = upper_floor_area * (floors - 2)
        total_area = ground_floor_area + repeated_floors_total_area + top_floor_area

        # Financial parameters
        land_price_per_sqm = 5000
        construction_cost_per_sqm = 2500
        sale_price_per_sqm = 8000
        
        # Store sizes
        min_store_size = 30
        max_store_size = 200
        avg_store_size = (min_store_size + max_store_size) / 2
        store_units = total_area / avg_store_size

        # Cost calculations
        total_land_cost = land_area * land_price_per_sqm
        total_construction_cost = total_area * construction_cost_per_sqm
        design_cost = 500000
        legal_cost = 300000
        landscaping_cost = 200000
        
        total_construction_with_additional = (
            total_construction_cost + 
            design_cost + 
            legal_cost + 
            landscaping_cost
        )
        
        total_investment = total_land_cost + total_construction_with_additional
        
        # Revenue calculations
        total_sales_revenue = total_area * sale_price_per_sqm
        gross_profit = total_sales_revenue - total_investment
        profit_margin_percentage = (gross_profit / total_investment) * 100
        
        # Rental calculations
        annual_rent_per_sqm = land_price_per_sqm * 0.18
        total_annual_rent = total_area * annual_rent_per_sqm
        operating_expenses = total_annual_rent * 0.20
        net_annual_rent = total_annual_rent - operating_expenses
        rental_roi = (net_annual_rent / total_investment) * 100

        return {
            "مقدمة": "تمثل هذه الدراسة تحليلاً شاملاً لفرصة استثمارية في تطوير مول تجاري حديث. يهدف المشروع إلى تلبية احتياجات السوق المتزايدة للمساحات التجارية العصرية.",
            "العنوان": f"دراسة جدوى استثمارية لمول تجاري في {location}",
            "تقرير_تحليل_الاستثمار": {
                "مقدمة": "هذا التحليل الاستثماري المفصل يقيم جدوى وربحية تطوير مول تجاري عصري. يشمل التحليل دراسة السوق المستهدف، وتقديرات التكاليف، وتوقعات العوائد من التأجير والاستثمار.",
                "تفاصيل_المشروع": {
                    "الموقع": location,
                    "مساحة_الأرض_الإجمالية": f"{self.format_number(land_area)} متر مربع",
                    "نوع_المشروع": "مول تجاري",
                    "تنظيمات_التخطيط": f"يسمح ببناء {floors} طوابق"
                },
                "معايير_التطوير": {
                    "نسبة_البناء_للدور_الأرضي": f"{ratios.ground_floor * 100}%",
                    "نسبة_البناء_للأدوار_المتكررة": f"{ratios.upper_floors * 100}%",
                    "نسبة_البناء_للملحق_العلوي": f"{ratios.top_floor * 100}%",
                    "الطوابق_المقترحة": f"{floors}",
                    "مساحة_البناء_الفعالة_للدور_الأرضي": f"مساحة_الأرض_الإجمالية * نسبة_البناء_للدور_الأرضي = {self.format_number(land_area)} * {ratios.ground_floor} = {self.format_number(ground_floor_area)} متر مربع",
                    "مساحة_البناء_الفعالة_للمتكرر": f"مساحة_الأرض_الإجمالية * نسبة_البناء_للأدوار_المتكررة = {self.format_number(land_area)} * {ratios.upper_floors} = {self.format_number(upper_floor_area)} متر مربع",
                    "مساحة_البناء_الفعالة_للملحق_العلوي": f"مساحة_البناء_الفعالة_للمتكرر * نسبة_البناء_للملحق_العلوي = {self.format_number(upper_floor_area)} * {ratios.top_floor} = {self.format_number(top_floor_area)} متر مربع",
                    "مساحة_البناء_الفعالة_للأدوار_المتكررة": f"مساحة_البناء_الفعالة_للمتكرر * (الطوابق_المقترحة - 2) = {self.format_number(upper_floor_area)} * ({floors} - 2) = {self.format_number(repeated_floors_total_area)} متر مربع",
                    "نتيجة_مساحة_البناء_الفعالة": f"{self.format_number(total_area)} متر مربع",
                    "معامل_البناء": f"نتيجة_مساحة_البناء_الفعالة / مساحة_الأرض_الإجمالية = {self.format_number(total_area)} / {self.format_number(land_area)} = {total_area/land_area:.2f}",
                    "نتيجة_معامل_البناء": f"{total_area/land_area:.2f}",
                    "نطاق_حجم_الوحدات_التجارية": f"من {min_store_size} إلى {max_store_size} متر مربع",
                    "الوحدات_التجارية_المقترحة": f"نتيجة_مساحة_البناء_الفعالة / متوسط_مساحة_الوحدة = {self.format_number(total_area)} / {avg_store_size:.1f}",
                    "نتيجة_الوحدات_التجارية_المقترحة": f"{int(store_units)} وحدة تجارية"
                },
                "توقعات_التمويل": {
                    "تكلفة_شراء_الأرض": {
                        "تكلفة_الشراء_لكل_متر_مربع": f"{self.format_number(land_price_per_sqm)} ريال سعودي",
                        "التكلفة_الكلية": f"مساحة_الأرض_الإجمالية * تكلفة_الشراء_لكل_متر_مربع = {self.format_number(land_area)} * {self.format_number(land_price_per_sqm)} = {self.format_number(total_land_cost)} ريال سعودي",
                        "نتيجة_التكلفة_الكلية": f"{self.format_number(total_land_cost)} ريال سعودي"
                    },
                    "تكاليف_البناء": {
                        "تكلفة_البناء_لكل_متر_مربع": f"{self.format_number(construction_cost_per_sqm)} ريال سعودي",
                        "مجموع_تكاليف_البناء": f"نتيجة_مساحة_البناء_الفعالة * تكلفة_البناء_لكل_متر_مربع = {self.format_number(total_area)} * {self.format_number(construction_cost_per_sqm)} = {self.format_number(total_construction_cost)} ريال سعودي",
                        "نتيجة_مجموع_تكاليف_البناء": f"{self.format_number(total_construction_cost)} ريال سعودي",
                        "التكاليف_الإضافية": {
                            "تصميم_معماري": f"{self.format_number(design_cost)} ريال سعودي",
                            "قانوني_وإداري": f"{self.format_number(legal_cost)} ريال سعودي",
                            "تنسيق_الموقع": f"{self.format_number(landscaping_cost)} ريال سعودي"
                        },
                        "المجموع": f"مجموع_تكاليف_البناء + تصميم_معماري + قانوني_وإداري + تنسيق_الموقع = {self.format_number(total_construction_with_additional)} ريال سعودي",
                        "نتيجة_المجموع": f"{self.format_number(total_construction_with_additional)} ريال سعودي"
                    },
                    "الاستثمار_الكلي": f"تكلفة_شراء_الأرض + مجموع_تكاليف_البناء = {self.format_number(total_land_cost)} + {self.format_number(total_construction_with_additional)}",
                    "نتيجة_الاستثمار_الكلي": f"{self.format_number(total_investment)} ريال سعودي",
                    "توقعات_الإيرادات_من_البيع": {
                        "سعر_البيع_لكل_متر_مربع": f"{self.format_number(sale_price_per_sqm)} ريال سعودي",
                        "إيرادات_محتملة_من_البيع": f"نتيجة_مساحة_البناء_الفعالة * سعر_البيع_لكل_متر_مربع = {self.format_number(total_area)} * {self.format_number(sale_price_per_sqm)} = {self.format_number(total_sales_revenue)} ريال سعودي",
                        "نتيجة_الإيرادات_المحتملة_من_البيع": f"{self.format_number(total_sales_revenue)} ريال سعودي",
                        "هامش_الربح_الإجمالي": f"إيرادات_محتملة_من_البيع - الاستثمار_الكلي = {self.format_number(total_sales_revenue)} - {self.format_number(total_investment)}",
                        "نتيجة_هامش_الربح_الإجمالي": f"{self.format_number(gross_profit)} ريال سعودي",
                        "نسبة_هامش_الربح_الإجمالي": f"{profit_margin_percentage:.2f}%"
                    },
                    "توقعات_الإيرادات_من_الإيجار": {
                        "الإيجار_السنوي_المتوقع_لكل_متر_مربع": f"{self.format_number(annual_rent_per_sqm)} ريال سعودي",
                        "الإيجار_السنوي_الكلي": f"نتيجة_مساحة_البناء_الفعالة * الإيجار_السنوي_المتوقع_لكل_متر_مربع = {self.format_number(total_area)} * {self.format_number(annual_rent_per_sqm)} = {self.format_number(total_annual_rent)} ريال سعودي",
                        "نتيجة_الإيجار_السنوي_الكلي": f"{self.format_number(total_annual_rent)} ريال سعودي",
                        "النفقات_التشغيلية": f"20% من الإيجار_السنوي_الكلي = {self.format_number(operating_expenses)} ريال سعودي",
                        "نتيجة_النفقات_التشغيلية": f"{self.format_number(operating_expenses)} ريال سعودي",
                        "صافي_الإيجار_السنوي": f"{self.format_number(net_annual_rent)} ريال سعودي",
                        "عائد_الاستثمار_من_الإيجار": f"{rental_roi:.2f}%"
                    }
                },
                "تقييم_المخاطر": {
                    "تقلبات_السوق": "متوسطة - يتأثر قطاع التجزئة بالتغيرات الاقتصادية وأنماط المستهلكين",
                    "التغييرات_التنظيمية": "منخفضة - القطاع التجاري يتمتع باستقرار تنظيمي",
                    "العوامل_الاقتصادية": "متوسطة - تعتمد على القوة الشرائية والنمو الاقتصادي"
                },
                "اعتبارات_استراتيجية": {
                    "اتجاهات_السوق": "نمو متزايد في قطاع التجزئة مع تطور أنماط التسوق",
                    "توقيت_الاستثمار": "مناسب مع تزايد الطلب على المراكز التجارية الحديثة",
                    "التوقعات_طويلة_الأمد": "إيجابية مع استمرار نمو قطاع التجزئة"
                },
                "ملخص_تنفيذي": "يمثل المشروع فرصة استثمارية واعدة في قطاع المراكز التجارية المتنامي",
                "توصيات": "يوصى بالمضي قدماً في المشروع مع التركيز على جذب المستأجرين الرئيسيين وتنويع المحلات التجارية"
            },
            "ملخص_تنفيذي": "يقدم المشروع فرصة استثمارية جذابة في قطاع المراكز التجارية مع توقعات عوائد مجزية وإمكانات نمو واعدة"
        }

    def _generate_risk_assessment(self) -> dict:
            """Generate risk assessment section"""
            return {
                "تقلبات_السوق": "متوسطة - يواجه سوق العقارات في الرياض تقلبات دورية.",
                "التغييرات_التنظيمية": "مخاطر منخفضة - بيئة تنظيمية مستقرة مع توقعات بتغييرات طفيفة.",
                "العوامل_الاقتصادية": "عالية - قد تؤثر التنويع الاقتصادي والاستثمار العام بشكل كبير على قيم العقارات."
            }

    def _generate_strategic_considerations(self) -> dict:
            """Generate strategic considerations section"""
            return {
                "اتجاهات_السوق": "يشهد سوق العقارات في الرياض حالياً اتجاهاً تصاعدياً، مدعوماً بالإصلاحات الاقتصادية وزيادة الاستثمار الأجنبي.",
                "توقيت_الاستثمار": "مثالي - تقدم ظروف السوق الحالية والنمو الاقتصادي المتوقع بيئة مواتية لبدء التطوير.",
                "التوقعات_طويلة_الأمد": "إمكانية تقدير القيمة طويلة الأمد قوية، مما يجعلها استثمارًا جذابًا لكل من العوائد الفورية والمستقبلية."
            }

    def _generate_executive_summary(self, location: str) -> str:
            """Generate executive summary"""
            return f"""يمثل التطوير المقترح في {location} استثمارًا استراتيجيًا سليمًا مع استراتيجية إيرادية مزدوجة من خلال المبيعات والإيجارات. 
            تشير التوقعات المالية إلى عائد استثماري صلب مع مخاطر قابلة للإدارة، متماشية مع ديناميكيات السوق الحالية وآفاق النمو المستقبلية. 
            يُوصى ببدء المشروع على الفور للاستفادة من ظروف السوق المواتية."""

    def _generate_recommendations(self) -> str:
            """Generate recommendations"""
            return """المضي قدماً في الاستحواذ والتطوير، مع ضمان إدارة صارمة للتكاليف والالتزام بالجداول الزمنية المتوقعة لتعظيم الربحية. 
            يُنصح بمراقبة مستمرة لظروف السوق وإعادة تقييم منتظمة للاتجاهات الاستراتيجية."""

    def format_number(self, number: float) -> str:
            return f"{number:,.0f}"

    def calculate_residential_context(self, land_area: float, location: str, floors: int) -> dict:
            """Calculate residential investment analysis with detailed breakdowns"""
            
            # Initialize building ratios
            ratios = BuildingRatios.create(floors)
            
            # Calculate areas
            ground_floor_area = land_area * ratios.ground_floor
            repeated_floor_area = land_area * ratios.upper_floors
            top_floor_area = repeated_floor_area * ratios.top_floor
            total_repeated_area = repeated_floor_area * (floors - 1)
            total_area = ground_floor_area + total_repeated_area + top_floor_area

            # Financial calculations
            land_price_per_sqm = self.location_prices.get(location, 5700)
            construction_cost_per_sqm = 1400
            
            # Calculate costs
            total_land_cost = land_area * land_price_per_sqm
            base_construction_cost = total_area * construction_cost_per_sqm
            
            additional_costs = {
                "تصميم_معماري": 200000,
                "قانوني_وإداري": 150000,
                "تنسيق_الموقع": 100000
            }


            total_additional = sum(additional_costs.values())
            total_construction = base_construction_cost + total_additional
            total_investment = total_land_cost + total_construction

            # Revenue calculations
            selling_price_per_sqm = land_price_per_sqm * 1.2
            total_sales = total_area * selling_price_per_sqm
            gross_margin = total_sales - total_investment
            margin_percentage = (gross_margin / total_investment) * 100

            annual_rent_per_sqm = land_price_per_sqm * 0.09
            total_annual_rent = total_area * annual_rent_per_sqm
            operating_expenses = total_annual_rent * 0.20
            net_annual_rent = total_annual_rent - operating_expenses
            rental_roi = (net_annual_rent / total_investment) * 100

            return {
                "مقدمة": f"دراسة جدوى استثمارية لمشروع سكني في {location}",
                "تفاصيل_المشروع": {
                    "الموقع": location,
                    "مساحة_الأرض": f"{self.format_number(land_area)} متر مربع",
                    "عدد_الطوابق": floors,
                    "إجمالي_مساحة_البناء": f"{self.format_number(total_area)} متر مربع",
                    "معامل_البناء": f"{total_area/land_area:.2f}",
                    "الوحدات_السكنية_المقترحة": f"{int(total_area/135)}"
                },
                "معايير_التطوير": {
                    "نسبة_البناء_للدور_الأرضي": f"{ratios.ground_floor:.2f}",
                    "نسبة_البناء_للأدوار_المتكررة": f"{ratios.upper_floors:.2f}",
                    "نسبة_البناء_للملحق_العلوي": f"{ratios.top_floor:.2f}",
                    "مساحة_البناء_الفعالة": f"{self.format_number(total_area)} متر مربع",
                    "تفاصيل_المساحات": {
                        "الدور_الأرضي": f"{self.format_number(ground_floor_area)} متر مربع",
                        "الأدوار_المتكررة": f"{self.format_number(total_repeated_area)} متر مربع",
                        "الملحق_العلوي": f"{self.format_number(top_floor_area)} متر مربع"
                    }
                },
                "التكاليف": {
                    "تكلفة_الأرض": {
                        "سعر_المتر": f"{self.format_number(land_price_per_sqm)} ريال",
                        "الإجمالي": f"{self.format_number(total_land_cost)} ريال"
                    },
                    "تكلفة_البناء": {
                        "تكلفة_المتر": f"{self.format_number(construction_cost_per_sqm)} ريال",
                        "التكلفة_الأساسية": f"{self.format_number(base_construction_cost)} ريال",
                        "التكاليف_الإضافية": {k: f"{self.format_number(v)} ريال" for k, v in additional_costs.items()},
                        "الإجمالي": f"{self.format_number(total_construction)} ريال"
                    },
                    "إجمالي_الاستثمار": f"{self.format_number(total_investment)} ريال"
                },
                "العوائد": {
                    "البيع": {
                        "سعر_المتر": f"{self.format_number(selling_price_per_sqm)} ريال",
                        "إجمالي_المبيعات": f"{self.format_number(total_sales)} ريال",
                        "هامش_الربح": f"{self.format_number(gross_margin)} ريال",
                        "نسبة_الربحية": f"{margin_percentage:.2f}%"
                    },
                    "التأجير": {
                        "الإيجار_السنوي_للمتر": f"{self.format_number(annual_rent_per_sqm)} ريال",
                        "إجمالي_الإيجار_السنوي": f"{self.format_number(total_annual_rent)} ريال",
                        "النفقات_التشغيلية": f"{self.format_number(operating_expenses)} ريال",
                        "صافي_الإيجار_السنوي": f"{self.format_number(net_annual_rent)} ريال",
                        "عائد_الاستثمار": f"{rental_roi:.2f}%"
                    }
                },
                "تقييم_المخاطر": self._generate_risk_assessment(),
                "اعتبارات_استراتيجية": self._generate_strategic_considerations(),
                "ملخص_تنفيذي": self._generate_executive_summary(location),
                "توصيات": self._generate_recommendations()
            }

    def calculate_villa_analysis(self, land_area: float, location: str) -> dict:
         
        floors = 3  # عدد الطوابق المقترح
        ratios = SingleVillaBuildingRatios(floors)
        
        # Calculate building areas
        ground_floor_area = land_area * ratios.ground_floor
        first_floor_area = land_area * ratios.first_floor
        top_floor_area = first_floor_area * ratios.top_floor
        total_area = ground_floor_area + first_floor_area + top_floor_area

        return {
            "مقدمة": f"دراسة جدوى استثمارية لمشروع فيلا سكنية في {location}",
            "العنوان": f"مشروع تطوير فيلا سكنية في {location}",
            "تقرير_تحليل_الاستثمار": {
                "مقدمة": f"هذا التحليل الاستثماري المفصل يقيم جدوى وربحية تطوير مشروع فيلا فاخرة في {location} بالرياض. يشمل التحليل استراتيجيات البيع والإيجار، مع النظر في ديناميكيات السوق الحالية وتقديرات التكاليف والإمكانيات الإيرادية.",
                "تفاصيل_المشروع": {
                    "الموقع": f"{location}، الرياض",
                    "مساحة_الأرض_الإجمالية": f"{self.format_number(land_area)} متر مربع",
                    "نوع_المشروع": "تطوير سكني فردي",
                    "تنظيمات_التخطيط": f"يسمح ببناء حتى {floors} طوابق"
                },
                "معايير_التطوير": {
                    "نسبة_البناء_للدور_الأرضي": f"{ratios.ground_floor:.2f}",
                    "نسبة_البناء_للأدوار_المتكررة": f"{ratios.first_floor:.2f}",
                    "نسبة_البناء_للملحق_العلوي": f"{ratios.top_floor:.2f}",
                    "الطوابق_المقترحة": f"{floors}",
                    "مساحة_البناء_الفعالة_للدور_الأرضي": f"مساحة_الأرض_الإجمالية * نسبة_البناء_للدور_الأرضي: {self.format_number(land_area)} * {ratios.ground_floor:.2f} = {self.format_number(ground_floor_area)} متر مربع",
                    "مساحة_البناء_الفعالة_للمتكرر": f"مساحة_الأرض_الإجمالية * نسبة_البناء_للأدوار_المتكررة: {self.format_number(land_area)} * {ratios.first_floor:.2f} = {self.format_number(first_floor_area)} متر مربع",
                    "مساحة_البناء_الفعالة_للملحق_العلوي": f"مساحة_البناء_الفعالة_للمتكرر * نسبة_البناء_للملحق_العلوي: {self.format_number(first_floor_area)} * {ratios.top_floor:.2f} = {self.format_number(top_floor_area)} متر مربع",
                    "نتيجة_مساحة_البناء_الفعالة": f"{self.format_number(ground_floor_area)} + {self.format_number(first_floor_area)} + {self.format_number(top_floor_area)} = {self.format_number(total_area)} متر مربع",
                    "معامل_البناء": f"نتيجة_مساحة_البناء_الفعالة / مساحة_الأرض_الإجمالية: {self.format_number(total_area)} / {self.format_number(land_area)} = {total_area/land_area:.2f}",
                    "نتيجة_معامل_البناء": f"{total_area/land_area:.2f}"
                },
                                "توقعات_التمويل": {
                    "تكلفة_شراء_الأرض": {
                        "تكلفة_الشراء_لكل_متر_مربع": f"{self.format_number(self.location_prices[location])} ريال سعودي",
                        "التكلفة_الكلية": f"مساحة_الأرض_الإجمالية * تكلفة_الشراء_لكل_متر_مربع = {self.format_number(land_area)} * {self.format_number(self.location_prices[location])}",
                        "نتيجة_التكلفة_الكلية": f"{self.format_number(land_area * self.location_prices[location])} ريال سعودي"
                    },
                    "تكاليف_البناء": {
                        "تكلفة_البناء_لكل_متر_مربع": "1,400 ريال سعودي",
                        "مجموع_تكاليف_البناء": f"نتيجة_مساحة_البناء_الفعالة * تكلفة_البناء_لكل_متر_مربع = {self.format_number(total_area)} * 1,400",
                        "نتيجة_مجموع_تكاليف_البناء": f"{self.format_number(total_area * 1400)} ريال سعودي",
                        "التكاليف_الإضافية": {
                            "تصميم_معماري": "200,000 ريال سعودي",
                            "قانوني_وإداري": "150,000 ريال سعودي",
                            "تنسيق_الموقع": "100,000 ريال سعودي"
                        },
                        "مجموع_التكاليف_الإضافية": "450,000 ريال سعودي",
                        "المجموع": f"مجموع_تكاليف_البناء + مجموع_التكاليف_الإضافية = {self.format_number(total_area * 1400)} + 450,000",
                        "نتيجة_المجموع": f"{self.format_number(total_area * 1400 + 450000)} ريال سعودي"
                    },
                    "الاستثمار_الكلي": f"تكلفة_شراء_الأرض + مجموع_تكاليف_البناء = {self.format_number(land_area * self.location_prices[location])} + {self.format_number(total_area * 1400 + 450000)}",
                    "نتيجة_الاستثمار_الكلي": f"{self.format_number(land_area * self.location_prices[location] + total_area * 1400 + 450000)} ريال سعودي",
                    "توقعات_الإيرادات_من_البيع": {
                        "سعر_البيع_لكل_متر_مربع": f"{self.format_number(self.location_prices[location] * 1.2)} ريال سعودي",
                        "إيرادات_محتملة_من_البيع": f"نتيجة_مساحة_البناء_الفعالة * سعر_البيع_لكل_متر_مربع = {self.format_number(total_area)} * {self.format_number(self.location_prices[location] * 1.2)}",
                        "نتيجة_الإيرادات_المحتملة_من_البيع": f"{self.format_number(total_area * self.location_prices[location] * 1.2)} ريال سعودي",
                        "هامش_الربح_الإجمالي": f"إيرادات_محتملة_من_البيع - الاستثمار_الكلي = {self.format_number(total_area * self.location_prices[location] * 1.2)} - {self.format_number(land_area * self.location_prices[location] + total_area * 1400 + 450000)}",
                        "نتيجة_هامش_الربح_الإجمالي": f"{self.format_number(total_area * self.location_prices[location] * 1.2 - (land_area * self.location_prices[location] + total_area * 1400 + 450000))} ريال سعودي",
                        "نسبة_هامش_الربح_الإجمالي": f"{((total_area * self.location_prices[location] * 1.2 - (land_area * self.location_prices[location] + total_area * 1400 + 450000)) / (land_area * self.location_prices[location] + total_area * 1400 + 450000)) * 100:.2f}%"
                    },
                    "توقعات_الإيرادات_من_الإيجار": {
                        "الإيجار_السنوي_المتوقع_لكل_متر_مربع": f"{self.format_number(self.location_prices[location] * 0.09)} ريال سعودي",
                        "الإيجار_السنوي_الكلي": f"نتيجة_مساحة_البناء_الفعالة * الإيجار_السنوي_المتوقع_لكل_متر_مربع = {self.format_number(total_area)} * {self.format_number(self.location_prices[location] * 0.09)}",
                        "نتيجة_الإيجار_السنوي_الكلي": f"{self.format_number(total_area * self.location_prices[location] * 0.09)} ريال سعودي",
                        "النفقات_التشغيلية": f"20% من الإيجار_السنوي_الكلي = 0.20 * {self.format_number(total_area * self.location_prices[location] * 0.09)}",
                        "نتيجة_النفقات_التشغيلية": f"{self.format_number(total_area * self.location_prices[location] * 0.09 * 0.20)} ريال سعودي",
                        "صافي_الإيجار_السنوي": f"الإيجار_السنوي_الكلي - النفقات_التشغيلية = {self.format_number(total_area * self.location_prices[location] * 0.09)} - {self.format_number(total_area * self.location_prices[location] * 0.09 * 0.20)}",
                        "نتيجة_صافي_الإيجار_السنوي": f"{self.format_number(total_area * self.location_prices[location] * 0.09 * 0.80)} ريال سعودي",
                        "عائد_الاستثمار_من_الإيجار": f"صافي_الإيجار_السنوي / الاستثمار_الكلي * 100 = {self.format_number(total_area * self.location_prices[location] * 0.09 * 0.80)} / {self.format_number(land_area * self.location_prices[location] + total_area * 1400 + 450000)} * 100",
                        "نتيجة_عائد_الاستثمار_من_الإيجار": f"{(total_area * self.location_prices[location] * 0.09 * 0.80 / (land_area * self.location_prices[location] + total_area * 1400 + 450000)) * 100:.2f}%"
                    }
                },
                "تقييم_المخاطر": {
                    "تقلبات_السوق": "متوسطة - يواجه سوق العقارات في الرياض تقلبات دورية.",
                    "التغييرات_التنظيمية": "مخاطر منخفضة - بيئة تنظيمية مستقرة مع توقعات بتغييرات طفيفة.",
                    "العوامل_الاقتصادية": "عالية - قد تؤثر التنويع الاقتصادي والاستثمار العام بشكل كبير على قيم العقارات."
                },
                "اعتبارات_استراتيجية": {
                    "اتجاهات_السوق": "يشهد سوق العقارات في الرياض حالياً اتجاهاً تصاعدياً، مدعوماً بالإصلاحات الاقتصادية وزيادة الاستثمار الأجنبي.",
                    "توقيت_الاستثمار": "مثالي - تقدم ظروف السوق الحالية والنمو الاقتصادي المتوقع بيئة مواتية لبدء التطوير.",
                    "التوقعات_طويلة_الأمد": "إمكانية تقدير القيمة طويلة الأمد قوية، مما يجعلها استثمارًا جذابًا لكل من العوائد الفورية والمستقبلية."
                },
                "ملخص_تنفيذي": f"يمثل التطوير المقترح في {location} استثمارًا استراتيجيًا سليمًا مع استراتيجية إيرادية مزدوجة من خلال المبيعات والإيجارات. تشير التوقعات المالية إلى عائد استثماري صلب مع مخاطر قابلة للإدارة.",
                "توصيات": "المضي قدماً في الاستحواذ والتطوير، مع ضمان إدارة صارمة للتكاليف والالتزام بالجداول الزمنية المتوقعة لتعظيم الربحية."
            },
            "ملخص_تنفيذي": f"مشروع تطوير فيلا سكنية في {location} يمثل فرصة استثمارية واعدة مع توقعات عوائد جيدة"
        }


    def calculate_compound_analysis(self, land_area: float, location: str, effective_land_ratio: float = 0.40) -> dict:
    # Initialize variables
        floors = 4  # عدد الطوابق المقترح
        ratios = CompoundBuildingRatios(floors)
        
        # Calculate effective building areas
        effective_land_area = land_area * effective_land_ratio
        proposed_buildings = 4  # عدد العمارات المقترح
        building_area = effective_land_area / proposed_buildings
        
        # Calculate building areas per floor
        ground_floor_area = building_area * ratios.ground_floor
        first_floor_area = building_area * ratios.first_floor
        repeated_floors_area = first_floor_area * (floors - 2)  # للطوابق المتكررة
        top_floor_area = first_floor_area * ratios.top_floor
        
        # Calculate total areas
        total_building_area = ground_floor_area + repeated_floors_area + top_floor_area
        total_compound_area = total_building_area * proposed_buildings
        
        # Calculate units
        avg_unit_size = 120  # متوسط مساحة الوحدة السكنية
        units_per_building = int(total_building_area / avg_unit_size)
        total_units = units_per_building * proposed_buildings

        return {
            "مقدمة": f"دراسة جدوى استثمارية لمشروع مجمع سكني في {location}",
            "العنوان": f"مشروع تطوير مجمع سكني في {location}",
            "تقرير_تحليل_الاستثمار": {
                "مقدمة": f"هذا التحليل الاستثماري المفصل يقيم جدوى وربحية تطوير مشروع مجمع سكني في {location} بالرياض. يشمل التحليل استراتيجيات البيع والإيجار، مع النظر في ديناميكيات السوق الحالية وتقديرات التكاليف والإمكانيات الإيرادية.",
                "تفاصيل_المشروع": {
                    "الموقع": f"{location}، الرياض",
                    "مساحة_الأرض_الإجمالية": f"{self.format_number(land_area)} متر مربع",
                    "نوع_المشروع": "تطوير مجمع سكني",
                    "عدد_العمارات_المقترحة": f"{proposed_buildings} عمارات",
                    "تنظيمات_التخطيط": f"يسمح ببناء حتى {floors} طوابق"
                },
                "معايير_التطوير": {
                    "نسبة_البناء_الفعالة_على_الأرض": f"{effective_land_ratio * 100}%",
                    "مساحة_الأرض_الفعالة_للبناء": f"{self.format_number(effective_land_area)} متر مربع",
                    "مساحة_العمارة": f"{self.format_number(building_area)} متر مربع",
                    "معامل_البناء_للأرض": f"{effective_land_ratio:.2f}",
                    "نسبة_البناء_للدور_الأرضي": f"{ratios.ground_floor:.2f}",
                    "نسبة_البناء_للأدوار_المتكررة": f"{ratios.first_floor:.2f}",
                    "نسبة_البناء_للملحق_العلوي": f"{ratios.top_floor:.2f}",
                    "الطوابق_المقترحة": f"{floors}",
                    "مساحة_البناء_الفعالة_للدور_الأرضي": f"{self.format_number(ground_floor_area)} متر مربع",
                    "مساحة_البناء_الفعالة_للمتكرر": f"{self.format_number(first_floor_area)} متر مربع",
                    "مساحة_البناء_الفعالة_للملحق_العلوي": f"{self.format_number(top_floor_area)} متر مربع",
                    "مساحة_البناء_الفعالة_للأدوار_المتكررة": f"{self.format_number(repeated_floors_area)} متر مربع",
                    "نتيجة_مساحة_البناء_الفعالة_للعمارة": f"{self.format_number(total_building_area)} متر مربع",
                    "معامل_البناء": f"{total_compound_area/land_area:.2f}",
                    "مجموع_مساحة_البناء_الفعالة_للكومباوند": f"{self.format_number(total_compound_area)} متر مربع",
                    "نطاق_حجم_الوحدات_السكنية": "90 إلى 150 متر مربع",
                    "الوحدات_السكنية_المقترحة_لكل_عمارة": f"{units_per_building}",
                    "عدد_الوحدات_السكنية_في_المشروع": f"{total_units}"
                },
                "توقعات_التمويل": {
                    "تكلفة_شراء_الأرض": {
                            "تكلفة_الشراء_لكل_متر_مربع": f"{self.format_number(self.location_prices[location])} ريال سعودي",
                            "التكلفة_الكلية": f"مساحة_الأرض_الإجمالية * تكلفة_الشراء_لكل_متر_مربع = {self.format_number(land_area)} * {self.format_number(self.location_prices[location])}",
                            "نتيجة_التكلفة_الكلية": f"{self.format_number(land_area * self.location_prices[location])} ريال سعودي"
                        },
                    "تكاليف_البناء": {
                        "تكلفة_البناء_لكل_متر_مربع": "1,400 ريال سعودي",
                        "مجموع_تكاليف_البناء": f"مجموع_مساحة_البناء_الفعالة_للكومباوند * تكلفة_البناء_لكل_متر_مربع = {self.format_number(total_compound_area)} * 1,400",
                        "نتيجة_مجموع_تكاليف_البناء": f"{self.format_number(total_compound_area * 1400)} ريال سعودي",
                        "التكاليف_الإضافية": {
                            "تصميم_معماري": "200,000 ريال سعودي",
                            "قانوني_وإداري": "150,000 ريال سعودي",
                            "تنسيق_الموقع": "100,000 ريال سعودي"
                        },
                        "مجموع_التكاليف_الإضافية": "450,000 ريال سعودي",
                        "المجموع": f"مجموع_تكاليف_البناء + مجموع_التكاليف_الإضافية = {self.format_number(total_compound_area * 1400)} + 450,000",
                        "نتيجة_المجموع": f"{self.format_number(total_compound_area * 1400 + 450000)} ريال سعودي"
                    },
                                        "الاستثمار_الكلي": f"تكلفة_شراء_الأرض + مجموع_تكاليف_البناء = {self.format_number(land_area * self.location_prices[location])} + {self.format_number(total_compound_area * 1400 + 450000)}",
                    "نتيجة_الاستثمار_الكلي": f"{self.format_number(land_area * self.location_prices[location] + total_compound_area * 1400 + 450000)} ريال سعودي",
                    "توقعات_الإيرادات_من_البيع": {
                        "سعر_البيع_لكل_متر_مربع": f"{self.format_number(self.location_prices[location] * 1.3)} ريال سعودي",
                        "إيرادات_محتملة_من_البيع": f"مجموع_مساحة_البناء_الفعالة_للكومباوند * سعر_البيع_لكل_متر_مربع = {self.format_number(total_compound_area)} * {self.format_number(self.location_prices[location] * 1.3)}",
                        "نتيجة_الإيرادات_المحتملة_من_البيع": f"{self.format_number(total_compound_area * self.location_prices[location] * 1.3)} ريال سعودي",
                        "هامش_الربح_الإجمالي": f"إيرادات_محتملة_من_البيع - الاستثمار_الكلي = {self.format_number(total_compound_area * self.location_prices[location] * 1.3)} - {self.format_number(land_area * self.location_prices[location] + total_compound_area * 1400 + 450000)}",
                        "نتيجة_هامش_الربح_الإجمالي": f"{self.format_number(total_compound_area * self.location_prices[location] * 1.3 - (land_area * self.location_prices[location] + total_compound_area * 1400 + 450000))} ريال سعودي",
                        "نسبة_هامش_الربح_الإجمالي": f"{((total_compound_area * self.location_prices[location] * 1.3 - (land_area * self.location_prices[location] + total_compound_area * 1400 + 450000)) / (land_area * self.location_prices[location] + total_compound_area * 1400 + 450000)) * 100:.2f}%"
                    },
                    "توقعات_الإيرادات_من_الإيجار": {
                        "الإيجار_السنوي_المتوقع_لكل_متر_مربع": f"{self.format_number(self.location_prices[location] * 0.09)} ريال سعودي",
                        "الإيجار_السنوي_الكلي": f"مجموع_مساحة_البناء_الفعالة_للكومباوند * الإيجار_السنوي_المتوقع_لكل_متر_مربع = {self.format_number(total_compound_area)} * {self.format_number(self.location_prices[location] * 0.09)}",
                        "نتيجة_الإيجار_السنوي_الكلي": f"{self.format_number(total_compound_area * self.location_prices[location] * 0.09)} ريال سعودي",
                        "النفقات_التشغيلية": f"20% من الإيجار_السنوي_الكلي = 0.20 * {self.format_number(total_compound_area * self.location_prices[location] * 0.09)}",
                        "نتيجة_النفقات_التشغيلية": f"{self.format_number(total_compound_area * self.location_prices[location] * 0.09 * 0.20)} ريال سعودي",
                        "صافي_الإيجار_السنوي": f"الإيجار_السنوي_الكلي - النفقات_التشغيلية = {self.format_number(total_compound_area * self.location_prices[location] * 0.09)} - {self.format_number(total_compound_area * self.location_prices[location] * 0.09 * 0.20)}",
                        "نتيجة_صافي_الإيجار_السنوي": f"{self.format_number(total_compound_area * self.location_prices[location] * 0.09 * 0.80)} ريال سعودي",
                        "عائد_الاستثمار_من_الإيجار": f"صافي_الإيجار_السنوي / الاستثمار_الكلي * 100 = {self.format_number(total_compound_area * self.location_prices[location] * 0.09 * 0.80)} / {self.format_number(land_area * self.location_prices[location] + total_compound_area * 1400 + 450000)} * 100",
                        "نتيجة_عائد_الاستثمار_من_الإيجار": f"{(total_compound_area * self.location_prices[location] * 0.09 * 0.80 / (land_area * self.location_prices[location] + total_compound_area * 1400 + 450000)) * 100:.2f}%"
                    }
                },
                "تقييم_المخاطر": {
                    "تقلبات_السوق": "متوسطة - يواجه سوق العقارات في الرياض تقلبات دورية.",
                    "التغييرات_التنظيمية": "مخاطر منخفضة - بيئة تنظيمية مستقرة مع توقعات بتغييرات طفيفة.",
                    "العوامل_الاقتصادية": "عالية - قد تؤثر التنويع الاقتصادي والاستثمار العام بشكل كبير على قيم العقارات."
                },
                "اعتبارات_استراتيجية": {
                    "اتجاهات_السوق": "يشهد سوق العقارات في الرياض حالياً اتجاهاً تصاعدياً، مدعوماً بالإصلاحات الاقتصادية وزيادة الاستثمار الأجنبي.",
                    "توقيت_الاستثمار": "مثالي - تقدم ظروف السوق الحالية والنمو الاقتصادي المتوقع بيئة مواتية لبدء التطوير.",
                    "التوقعات_طويلة_الأمد": "إمكانية تقدير القيمة طويلة الأمد قوية، مما يجعلها استثمارًا جذابًا لكل من العوائد الفورية والمستقبلية."
                },
                "ملخص_تنفيذي": f"يمثل التطوير المقترح في {location} استثمارًا استراتيجيًا سليمًا مع استراتيجية إيرادية مزدوجة من خلال المبيعات والإيجارات. يتضمن المشروع {proposed_buildings} عمارات بإجمالي {total_units} وحدة سكنية.",
                "توصيات": "المضي قدماً في الاستحواذ والتطوير، مع ضمان إدارة صارمة للتكاليف والالتزام بالجداول الزمنية المتوقعة لتعظيم الربحية."
            },
            "ملخص_تنفيذي": f"مشروع تطوير مجمع سكني في {location} يمثل فرصة استثمارية واعدة مع {total_units} وحدة سكنية وتوقعات عوائد جيدة"
        }


    def calculate_villa_context(self, land_area: float, location: str) -> dict:
        """Calculate villa investment analysis with detailed breakdowns"""
        # Initialize variables
        villa_area = 300  # مساحة الفيلا النموذجية
        floors = 3  # عدد الطوابق المقترح
        ratios = VillaBuildingRatios.create(floors)
        
        # Calculate areas
        effective_land_ratio = 0.40
        effective_land_area = land_area * effective_land_ratio
        
        # Calculate building areas
        ground_floor_area = villa_area * ratios.ground_floor
        first_floor_area = villa_area * ratios.first_floor
        top_floor_area = first_floor_area * ratios.top_floor
        
        # Calculate total areas
        total_villa_area = ground_floor_area + first_floor_area + top_floor_area
        proposed_villas = int(effective_land_area / villa_area)
        total_compound_area = total_villa_area * proposed_villas
        
        return {
            "مقدمة": f"دراسة جدوى استثمارية لمشروع مجمع فلل سكنية في {location}",
            "العنوان": f"مشروع تطوير مجمع فلل سكنية في {location}",
            "تقرير_تحليل_الاستثمار": {
                "مقدمة": f"هذا التحليل الاستثماري المفصل يقيم جدوى وربحية تطوير مشروع فلل فاخر في {location} بالرياض. يشمل التحليل استراتيجيات البيع والإيجار، مع النظر في ديناميكيات السوق الحالية وتقديرات التكاليف والإمكانيات الإيرادية.",
                "تفاصيل_المشروع": {
                    "الموقع": f"{location}، الرياض",
                    "مساحة_الأرض_الإجمالية": f"{self.format_number(land_area)} متر مربع",
                    "نوع_المشروع": "تطوير سكني فردي",
                    "تنظيمات_التخطيط": f"يسمح ببناء حتى {floors} طوابق"
                },
                "معايير_التطوير": {
                    "نسبة_البناء_الفعالة_على_الأرض": f"{effective_land_ratio * 100}%",
                    "مساحة_الأرض_الفعالة_للبناء": f"مساحة_الأرض_الإجمالية * نسبة_البناء_الفعالة_على_الأرض: {self.format_number(land_area)} * {effective_land_ratio} = {self.format_number(effective_land_area)} متر مربع",
                    "مساحة_الفيلا": f"{self.format_number(villa_area)} متر مربع",
                    "معامل_البناء_للأرض": f"مساحة_الأرض_الفعالة_للبناء / مساحة_الأرض_الإجمالية: {self.format_number(effective_land_area)} / {self.format_number(land_area)}",
                    "نتيجة_معامل_البناء_للأرض": f"{effective_land_ratio:.2f}",
                    "نسبة_البناء_للدور_الأرضي": f"{ratios.ground_floor:.2f}",
                    "نسبة_البناء_للأدوار_المتكررة": f"{ratios.first_floor:.2f}",
                    "نسبة_البناء_للملحق_العلوي": f"{ratios.top_floor:.2f}",
                    "الطوابق_المقترحة": f"{floors}",
                    "مساحة_البناء_الفعالة_للدور_الأرضي": f"مساحة_الفيلا * نسبة_البناء_للدور_الأرضي: {self.format_number(villa_area)} * {ratios.ground_floor:.2f} = {self.format_number(ground_floor_area)} متر مربع",
                    "مساحة_البناء_الفعالة_للمتكرر": f"مساحة_الفيلا * نسبة_البناء_للأدوار_المتكررة: {self.format_number(villa_area)} * {ratios.first_floor:.2f} = {self.format_number(first_floor_area)} متر مربع",
                    "مساحة_البناء_الفعالة_للملحق_العلوي": f"مساحة_البناء_الفعالة_للمتكرر * نسبة_البناء_للملحق_العلوي: {self.format_number(first_floor_area)} * {ratios.top_floor:.2f} = {self.format_number(top_floor_area)} متر مربع",
                    "نتيجة_مساحة_البناء_الفعالة": f"{self.format_number(total_villa_area)} متر مربع",
                    "عدد_الفلل_المقترح": f"مساحة_الأرض_الفعالة_للبناء / مساحة_الفيلا: {self.format_number(effective_land_area)} / {self.format_number(villa_area)} = {proposed_villas}",
                    "مجموع_مساحة_البناء_الفعالة_للكومباوند": f"نتيجة_مساحة_البناء_الفعالة * عدد_الفلل_المقترح: {self.format_number(total_villa_area)} * {proposed_villas} = {self.format_number(total_compound_area)} متر مربع",
                    "معامل_البناء": f"مجموع_مساحة_البناء_الفعالة_للكومباوند / مساحة_الأرض_الإجمالية: {self.format_number(total_compound_area)} / {self.format_number(land_area)} = {total_compound_area/land_area:.2f}",
                    "نتيجة_معامل_البناء": f"{total_compound_area/land_area:.2f}",
                    "نتيجة_عدد_الفلل_المقترح": f"{proposed_villas}"
                },
                                "توقعات_التمويل": {
                    "تكلفة_شراء_الأرض": {
                        "تكلفة_الشراء_لكل_متر_مربع": f"{self.format_number(self.location_prices[location])} ريال سعودي",
                        "التكلفة_الكلية": f"مساحة_الأرض_الإجمالية * تكلفة_الشراء_لكل_متر_مربع = {self.format_number(land_area)} * {self.format_number(self.location_prices[location])}",
                        "نتيجة_التكلفة_الكلية": f"{self.format_number(land_area * self.location_prices[location])} ريال سعودي"
                    },
                    "تكاليف_البناء": {
                        "تكلفة_البناء_لكل_متر_مربع": "2,000 ريال سعودي",
                        "مجموع_تكاليف_البناء": f"مجموع_مساحة_البناء_الفعالة_للكومباوند * تكلفة_البناء_لكل_متر_مربع = {self.format_number(total_compound_area)} * 2,000",
                        "نتيجة_مجموع_تكاليف_البناء": f"{self.format_number(total_compound_area * 2000)} ريال سعودي",
                        "التكاليف_الإضافية": {
                            "تصميم_معماري": "200,000 ريال سعودي",
                            "قانوني_وإداري": "150,000 ريال سعودي",
                            "تنسيق_الموقع": "100,000 ريال سعودي"
                        },
                        "مجموع_التكاليف_الإضافية": "450,000 ريال سعودي",
                        "المجموع": f"مجموع_تكاليف_البناء + مجموع_التكاليف_الإضافية = {self.format_number(total_compound_area * 2000)} + 450,000",
                        "نتيجة_المجموع": f"{self.format_number(total_compound_area * 2000 + 450000)} ريال سعودي"
                    },
                    "الاستثمار_الكلي": f"تكلفة_شراء_الأرض + مجموع_تكاليف_البناء = {self.format_number(land_area * self.location_prices[location])} + {self.format_number(total_compound_area * 2000 + 450000)}",
                    "نتيجة_الاستثمار_الكلي": f"{self.format_number(land_area * self.location_prices[location] + total_compound_area * 2000 + 450000)} ريال سعودي",
                    "توقعات_الإيرادات_من_البيع": {
                        "سعر_البيع_لكل_متر_مربع": f"{self.format_number(self.location_prices[location] * 1.4)} ريال سعودي",
                        "إيرادات_محتملة_من_البيع": f"مجموع_مساحة_البناء_الفعالة_للكومباوند * سعر_البيع_لكل_متر_مربع = {self.format_number(total_compound_area)} * {self.format_number(self.location_prices[location] * 1.4)}",
                        "نتيجة_الإيرادات_المحتملة_من_البيع": f"{self.format_number(total_compound_area * self.location_prices[location] * 1.4)} ريال سعودي",
                        "هامش_الربح_الإجمالي": f"إيرادات_محتملة_من_البيع - الاستثمار_الكلي = {self.format_number(total_compound_area * self.location_prices[location] * 1.4)} - {self.format_number(land_area * self.location_prices[location] + total_compound_area * 2000 + 450000)}",
                        "نتيجة_هامش_الربح_الإجمالي": f"{self.format_number(total_compound_area * self.location_prices[location] * 1.4 - (land_area * self.location_prices[location] + total_compound_area * 2000 + 450000))} ريال سعودي",
                        "نسبة_هامش_الربح_الإجمالي": f"{((total_compound_area * self.location_prices[location] * 1.4 - (land_area * self.location_prices[location] + total_compound_area * 2000 + 450000)) / (land_area * self.location_prices[location] + total_compound_area * 2000 + 450000)) * 100:.2f}%"
                    },
                    "توقعات_الإيرادات_من_الإيجار": {
                        "الإيجار_السنوي_المتوقع_لكل_متر_مربع": f"{self.format_number(self.location_prices[location] * 0.08)} ريال سعودي",
                        "الإيجار_السنوي_الكلي": f"مجموع_مساحة_البناء_الفعالة_للكومباوند * الإيجار_السنوي_المتوقع_لكل_متر_مربع = {self.format_number(total_compound_area)} * {self.format_number(self.location_prices[location] * 0.08)}",
                        "نتيجة_الإيجار_السنوي_الكلي": f"{self.format_number(total_compound_area * self.location_prices[location] * 0.08)} ريال سعودي",
                        "النفقات_التشغيلية": f"20% من الإيجار_السنوي_الكلي = 0.20 * {self.format_number(total_compound_area * self.location_prices[location] * 0.08)}",
                        "نتيجة_النفقات_التشغيلية": f"{self.format_number(total_compound_area * self.location_prices[location] * 0.08 * 0.20)} ريال سعودي",
                        "صافي_الإيجار_السنوي": f"الإيجار_السنوي_الكلي - النفقات_التشغيلية = {self.format_number(total_compound_area * self.location_prices[location] * 0.08)} - {self.format_number(total_compound_area * self.location_prices[location] * 0.08 * 0.20)}",
                        "نتيجة_صافي_الإيجار_السنوي": f"{self.format_number(total_compound_area * self.location_prices[location] * 0.08 * 0.80)} ريال سعودي",
                        "عائد_الاستثمار_من_الإيجار": f"صافي_الإيجار_السنوي / الاستثمار_الكلي * 100 = {self.format_number(total_compound_area * self.location_prices[location] * 0.08 * 0.80)} / {self.format_number(land_area * self.location_prices[location] + total_compound_area * 2000 + 450000)} * 100",
                        "نتيجة_عائد_الاستثمار_من_الإيجار": f"{(total_compound_area * self.location_prices[location] * 0.08 * 0.80 / (land_area * self.location_prices[location] + total_compound_area * 2000 + 450000)) * 100:.2f}%"
                    }
                },
                "تقييم_المخاطر": {
                    "تقلبات_السوق": "متوسطة - يواجه سوق العقارات في الرياض تقلبات دورية.",
                    "التغييرات_التنظيمية": "مخاطر منخفضة - بيئة تنظيمية مستقرة مع توقعات بتغييرات طفيفة.",
                    "العوامل_الاقتصادية": "عالية - قد تؤثر التنويع الاقتصادي والاستثمار العام بشكل كبير على قيم العقارات."
                },
                "اعتبارات_استراتيجية": {
                    "اتجاهات_السوق": "يشهد سوق العقارات في الرياض حالياً اتجاهاً تصاعدياً، مدعوماً بالإصلاحات الاقتصادية وزيادة الاستثمار الأجنبي.",
                    "توقيت_الاستثمار": "مثالي - تقدم ظروف السوق الحالية والنمو الاقتصادي المتوقع بيئة مواتية لبدء التطوير.",
                    "التوقعات_طويلة_الأمد": "إمكانية تقدير القيمة طويلة الأمد قوية، مما يجعلها استثمارًا جذابًا لكل من العوائد الفورية والمستقبلية."
                },
                "ملخص_تنفيذي": f"يمثل التطوير المقترح في {location} استثمارًا استراتيجيًا سليمًا مع استراتيجية إيرادية مزدوجة من خلال المبيعات والإيجارات. تشير التوقعات المالية إلى عائد استثماري صلب مع مخاطر قابلة للإدارة، متماشية مع ديناميكيات السوق الحالية وآفاق النمو المستقبلية.",
                "توصيات": "المضي قدماً في الاستحواذ والتطوير، مع ضمان إدارة صارمة للتكاليف والالتزام بالجداول الزمنية المتوقعة لتعظيم الربحية. يُنصح بمراقبة مستمرة لظروف السوق وإعادة تقييم منتظمة للاتجاهات الاستراتيجية."
            },
            "ملخص_تنفيذي": f"مشروع تطوير مجمع فلل سكنية في {location} يمثل فرصة استثمارية واعدة مع توقعات عوائد جيدة"
        }




    def calculate_commercial_context(self, land_area: float, location: str, floors: int) -> dict:
        ratios = CommercialRatios.create(floors)
        
        # Area calculations
        ground_floor_area = land_area * ratios.ground_floor
        upper_floor_area = land_area * ratios.upper_floors
        top_floor_area = upper_floor_area * ratios.top_floor
        repeated_floors_total_area = upper_floor_area * (floors - 2)
        total_area = ground_floor_area + repeated_floors_total_area + top_floor_area
        
        # Cost calculations
        land_price_per_sqm = 3500
        construction_cost_per_sqm = 1400
        total_land_cost = land_area * land_price_per_sqm
        total_construction_cost = total_area * construction_cost_per_sqm
        
        # Additional costs
        design_cost = 200000
        legal_cost = 150000
        landscaping_cost = 100000
        additional_costs = design_cost + legal_cost + landscaping_cost
        total_construction_with_additional = total_construction_cost + additional_costs
        
        # Total investment
        total_investment = total_land_cost + total_construction_with_additional

        # Commercial unit calculations
        min_unit_size = 50
        max_unit_size = 100
        avg_unit_size = 75
        commercial_units = total_area / avg_unit_size

        # Sales revenue calculations
        sale_price_per_sqm = 2500
        total_sales_revenue = total_area * sale_price_per_sqm
        gross_profit = total_sales_revenue - total_investment
        profit_margin_percentage = (gross_profit / total_investment) * 100

        # Rental calculations
        annual_rent_per_sqm = land_price_per_sqm * 0.18
        total_annual_rent = total_area * annual_rent_per_sqm
        operating_expenses = total_annual_rent * 0.20
        net_annual_rent = total_annual_rent - operating_expenses
        rental_roi = (net_annual_rent / total_investment) * 100

        return {
            "مقدمة": "تمثل هذه الدراسة حالة استثمارية لتطوير مبنى تجاري في موقع استراتيجي. تهدف هذه الدراسة إلى تحليل الجدوى المالية وتقدير العوائد المحتملة من المشروع.",
            "العنوان": "دراسة حالة استثمارية لتطوير مبنى تجاري",
            "تقرير_تحليل_الاستثمار": {
                "مقدمة": "هذا التحليل الاستثماري المفصل يقيم جدوى وربحية تطوير مشروع مبنى تجاري في موقع متميز. يشمل التحليل استراتيجيات البيع والإيجار، مع النظر في ديناميكيات السوق الحالية وتقديرات التكاليف والإمكانيات الإيرادية.",
                "تفاصيل_المشروع": {
                    "الموقع": "موقع استراتيجي",
                    "مساحة_الأرض_الإجمالية": f"{self.format_number(land_area)} متر مربع",
                    "نوع_المشروع": "تطوير مبنى تجاري",
                    "تنظيمات_التخطيط": f"يسمح ببناء حتى {floors} طوابق"
                },
                "معايير_التطوير": {
                    "نسبة_البناء_للدور_الأرضي": f"{ratios.ground_floor}",
                    "نسبة_البناء_للأدوار_المتكررة": f"{ratios.upper_floors}",
                    "نسبة_البناء_للملحق_العلوي": f"{ratios.top_floor}",
                    "الطوابق_المقترحة": f"{floors}",
                    "مساحة_البناء_الفعالة_للدور_الأرضي": f"مساحة_الأرض_الإجمالية * نسبة_البناء_للدور_الأرضي = {self.format_number(land_area)} * {ratios.ground_floor} = {self.format_number(ground_floor_area)} متر مربع",
                    "مساحة_البناء_الفعالة_للمتكرر": f"مساحة_الأرض_الإجمالية * نسبة_البناء_للأدوار_المتكررة = {self.format_number(land_area)} * {ratios.upper_floors} = {self.format_number(upper_floor_area)} متر مربع",
                    "مساحة_البناء_الفعالة_للملحق_العلوي": f"مساحة_البناء_الفعالة_للمتكرر * نسبة_البناء_للملحق_العلوي = {self.format_number(upper_floor_area)} * {ratios.top_floor} = {self.format_number(top_floor_area)} متر مربع",
                    "مساحة_البناء_الفعالة_للأدوار_المتكررة": f"مساحة_البناء_الفعالة_للمتكرر * (الطوابق_المقترحة - 2) = {self.format_number(upper_floor_area)} * ({floors} - 2) = {self.format_number(repeated_floors_total_area)} متر مربع",
                    "نتيجة_مساحة_البناء_الفعالة": f"مساحة_البناء_الفعالة_للدور_الأرضي + مساحة_البناء_الفعالة_للأدوار_المتكررة + مساحة_البناء_الفعالة_للملحق_العلوي = {self.format_number(ground_floor_area)} + {self.format_number(repeated_floors_total_area)} + {self.format_number(top_floor_area)} = {self.format_number(total_area)} متر مربع",
                    "معامل_البناء": f"نتيجة_مساحة_البناء_الفعالة / مساحة_الأرض_الإجمالية = {self.format_number(total_area)} / {self.format_number(land_area)} = {total_area/land_area:.3f}",
                    "نتيحة_معامل_البناء": f"{total_area/land_area:.3f}",
                    "نطاق_حجم_الوحدات-التجارية": f"'من {min_unit_size} إلى {max_unit_size} متر مربع'",
                    "الوحدات_التجارية_المقترحة": f"نتيجة_مساحة_البناء_الفعالة / متوسط مساحة الوحدة = {self.format_number(total_area)} / {avg_unit_size} = {int(commercial_units)} وحدات تقريبا",
                    "نتيجة_الوحدات_التجارية_المقترحة": f"{int(commercial_units)} وحدات تجارية"
                },
                                "توقعات_التمويل": {
                    "تكلفة_شراء_الأرض": {
                        "تكلفة_الشراء_لكل_متر_مربع": f"{self.format_number(land_price_per_sqm)} ريال سعودي",
                        "التكلفة_الكلية": f"مساحة_الأرض_الإجمالية * تكلفة_الشراء_لكل_متر_مربع = {self.format_number(land_area)} * {self.format_number(land_price_per_sqm)} = {self.format_number(total_land_cost)} ريال سعودي",
                        "نتيجة_التكلفة_الكلية": f"{self.format_number(total_land_cost)} ريال سعودي"
                    },
                    "تكاليف_البناء": {
                        "تكلفة_البناء_لكل_متر_مربع": f"{self.format_number(construction_cost_per_sqm)} ريال سعودي",
                        "مجموع_تكاليف_البناء": f"نتيجة_مساحة_البناء_الفعالة * تكلفة_البناء_لكل_متر_مربع = {self.format_number(total_area)} * {self.format_number(construction_cost_per_sqm)} = {self.format_number(total_construction_cost)} ريال سعودي",
                        "نتيجة_مجموع_تكاليف_البناء": f"{self.format_number(total_construction_cost)} ريال سعودي",
                        "التكاليف_الإضافية": {
                            "تصميم_معماري": f"{self.format_number(design_cost)} ريال سعودي",
                            "قانوني_وإداري": f"{self.format_number(legal_cost)} ريال سعودي",
                            "تنسيق_الموقع": f"{self.format_number(landscaping_cost)} ريال سعودي"
                        },
                        "المجموع": f"مجموع_تكاليف_البناء + تصميم_معماري + قانوني_وإداري + تنسيق_الموقع = {self.format_number(total_construction_cost)} + {self.format_number(design_cost)} + {self.format_number(legal_cost)} + {self.format_number(landscaping_cost)} = {self.format_number(total_construction_with_additional)} ريال سعودي",
                        "نتيجة_المجموع": f"{self.format_number(total_construction_with_additional)} ريال سعودي"
                    },
                    "الاستثمار_الكلي": f"تكلفة_شراء_الأرض + مجموع_تكاليف_البناء = {self.format_number(total_land_cost)} + {self.format_number(total_construction_with_additional)}",
                    "نتيجة_الاستثمار_الكلي": f"{self.format_number(total_investment)} ريال سعودي",
                    "توقعات_الإيرادات_من_البيع": {
                        "سعر_البيع_لكل_متر_مربع": f"يُقترح {self.format_number(sale_price_per_sqm)} ريال سعودي",
                        "إيرادات_محتملة_من_البيع": f"نتيجة_مساحة_البناء_الفعالة * سعر_البيع_لكل_متر_مربع = {self.format_number(total_area)} * {self.format_number(sale_price_per_sqm)} = {self.format_number(total_sales_revenue)} ريال سعودي",
                        "نتيجة_الإيرادات_المحتملة_من_البيع": f"{self.format_number(total_sales_revenue)} ريال سعودي",
                        "هامش_الربح_الإجمالي": f"إيرادات_محتملة_من_البيع - الاستثمار_الكلي = {self.format_number(total_sales_revenue)} - {self.format_number(total_investment)}",
                        "نتيجة_هامش_الربح_الإجمالي": f"{self.format_number(gross_profit)} ريال سعودي",
                        "نسبة_هامش_الربح_الإجمالي": f"هامش_الربح_الإجمالي / الاستثمار_الكلي * 100 = {self.format_number(gross_profit)} / {self.format_number(total_investment)} * 100",
                        "نتيجة_نسبة_هامش_الربح_الإجمالي": f"{profit_margin_percentage:.2f}%"
                    },
                    "توقعات_الإيرادات_من_الإيجار": {
                        "الإيجار_السنوي_المتوقع_لكل_متر_مربع": f"(18% من تكلفة_الشراء_لكل_متر_مربع) = {self.format_number(annual_rent_per_sqm)} ريال سعودي",
                        "الإيجار_السنوي_الكلي": f"نتيجة_مساحة_البناء_الفعالة * الإيجار_السنوي_المتوقع_لكل_متر_مربع = {self.format_number(total_area)} * {self.format_number(annual_rent_per_sqm)} = {self.format_number(total_annual_rent)} ريال سعودي",
                        "نتيجة_الإيجار_السنوي_الكلي": f"{self.format_number(total_annual_rent)} ريال سعودي",
                        "النفقات_التشغيلية": f"20% من الإيجار_السنوي_الكلي = 0.20 * {self.format_number(total_annual_rent)} = {self.format_number(operating_expenses)} ريال سعودي",
                        "نتيجة_النفقات_التشغيلية": f"{self.format_number(operating_expenses)} ريال سعودي",
                        "صافي_الإيجار_السنوي": f"الإيجار_السنوي_الكلي - النفقات_التشغيلية = {self.format_number(total_annual_rent)} - {self.format_number(operating_expenses)}",
                        "نتيجة_صافي_الإيجار_السنوي": f"{self.format_number(net_annual_rent)} ريال سعودي",
                        "عائد_الاستثمار_من_الإيجار": f"صافي_الإيجار_السنوي / الاستثمار_الكلي * 100 = {self.format_number(net_annual_rent)} / {self.format_number(total_investment)} * 100",
                        "نتيجة_عائد_الاستثمار_من_الإيجار": f"{rental_roi:.2f}%"
                    }
                },
                "تقييم_المخاطر": {
                    "تقلبات_السوق": "متوسطة - يواجه سوق العقارات تقلبات دورية.",
                    "التغييرات_التنظيمية": "مخاطر منخفضة - بيئة تنظيمية مستقرة مع توقعات بتغييرات طفيفة.",
                    "العوامل_الاقتصادية": "عالية - قد تؤثر التنويع الاقتصادي والاستثمار العام بشكل كبير على قيم العقارات."
                },
                "اعتبارات_استراتيجية": {
                    "اتجاهات_السوق": "يشهد سوق العقارات حالياً اتجاهاً تصاعدياً، مدعوماً بالإصلاحات الاقتصادية وزيادة الاستثمار الأجنبي.",
                    "توقيت_الاستثمار": "مثالي - تقدم ظروف السوق الحالية والنمو الاقتصادي المتوقع بيئة مواتية لبدء التطوير.",
                    "التوقعات_طويلة_الأمد": "إمكانية تقدير القيمة طويلة الأمد قوية، مما يجعلها استثمارًا جذابًا."
                },
                "ملخص_تنفيذي": "يمثل التطوير المقترح استثمارًا استراتيجيًا سليمًا مع استراتيجية إيرادية مزدوجة من خلال المبيعات والإيجارات. تشير التوقعات المالية إلى عائد استثماري صلب مع مخاطر قابلة للإدارة.",
                "توصيات": "المضي قدماً في الاستحواذ والتطوير مع ضمان إدارة صارمة للتكاليف."
            },
            "ملخص_تنفيذي": "يمثل هذا المشروع فرصة استثمارية جذابة بفضل موقعه الاستراتيجي وتوقعات العوائد الإيجابية. رغم وجود بعض المخاطر ، إلا أن هناك إمكانية كبيرة لتحقيق الأرباح في المستقبل القريب."
        }

    def calculate_mixed_use_context(self, land_area: float, location: str, floors: int) -> dict:
        ratios = MixedUseRatios.create(floors)
        
        # Area calculations
        ground_floor_area = land_area * ratios.ground_floor  # Commercial
        first_floor_area = land_area * ratios.first_floor    # Commercial
        repeated_floors_area = land_area * ratios.repeated_floors * (floors - 3)  # Residential
        top_floor_area = land_area * ratios.top_floor        # Residential
        
        total_commercial_area = ground_floor_area + first_floor_area
        total_residential_area = repeated_floors_area + top_floor_area
        total_area = total_commercial_area + total_residential_area

        # Cost calculations
        land_price_per_sqm = self.location_prices.get(location, 5700)
        commercial_construction_cost = 1800  # Higher for commercial
        residential_construction_cost = 1400
        construction_cost_per_sqm = (commercial_construction_cost + residential_construction_cost) / 2  # Average cost

        
        total_land_cost = land_area * land_price_per_sqm
        commercial_construction = total_commercial_area * commercial_construction_cost
        residential_construction = total_residential_area * residential_construction_cost
        total_construction_cost = commercial_construction + residential_construction

        # Additional costs
        additional_costs = {
            "تصميم": 300000,
            "قانوني": 200000,
            "تنسيق": 150000
        }
        total_additional = sum(additional_costs.values())

        # Define the missing variables:
        design_cost = additional_costs['تصميم']
        legal_cost = additional_costs['قانوني']
        landscaping_cost = additional_costs['تنسيق']

        total_additional = sum(additional_costs.values())

        total_construction_with_additional = total_construction_cost + total_additional
        total_investment = total_land_cost + total_construction_with_additional


        # Revenue calculations - Commercial
        commercial_sale_price_per_sqm = land_price_per_sqm * 1.4  # Define commercial_sale_price_per_sqm
        commercial_sales_revenue = total_commercial_area * commercial_sale_price_per_sqm
        commercial_rent_per_sqm = land_price_per_sqm * 0.12  # Define commercial_rent_per_sqm
        commercial_annual_rent = total_commercial_area * commercial_rent_per_sqm

        # Revenue calculations - Residential
        residential_sale_price_per_sqm = land_price_per_sqm * 1.2  # Define residential_sale_price_per_sqm
        residential_sales_revenue = total_residential_area * residential_sale_price_per_sqm
        residential_rent_per_sqm = land_price_per_sqm * 0.08  # Define residential_rent_per_sqm
        residential_annual_rent = total_residential_area * residential_rent_per_sqm

        # Combined revenues
        total_sales_revenue = commercial_sales_revenue + residential_sales_revenue
        total_annual_rent = commercial_annual_rent + residential_annual_rent
        operating_expenses = total_annual_rent * 0.20
        net_annual_rent = total_annual_rent - operating_expenses

        # Profitability calculations
        gross_profit = total_sales_revenue - total_investment
        profit_margin_percentage = (gross_profit / total_investment) * 100
        rental_roi = (net_annual_rent / total_investment) * 100

        return {
            "مقدمة": "تعتبر المشاريع السكنية والتجارية من المقومات الأساسية لتطوير المناطق الحضرية، حيث تسهم في تلبية احتياجات السكان وفي الوقت ذاته تعزز النشاط الاقتصادي. المشروع المقترح في حي النرجس بالرياض يعد فرصة استثمارية واعدة.",
            "العنوان": f"مشروع تطوير مبنى سكني تجاري في {location}",
            "تقرير_تحليل_الاستثمار": {
                "مقدمة": "هذا التحليل الاستثماري المفصل يقيم جدوى وربحية تطوير مشروع مبنى سكني تجاري فاخر في حي النرجس بالرياض. يشمل التحليل استراتيجيات البيع والإيجار، مع النظر في ديناميكيات السوق الحالية وتقديرات التكاليف والإمكانيات الإيرادية.",
                "تفاصيل_المشروع": {
                    "الموقع": f"{location}",
                    "مساحة_الأرض_الإجمالية": f"{self.format_number(land_area)} متر مربع",
                    "نوع_المشروع": "تطوير سكني وتجاري",
                    "تنظيمات_التخطيط": f"يسمح ببناء حتى {floors} طوابق"
                },
                "معايير_التطوير": {
                    "نسبة_البناء_للدور_الأرضي": f"{ratios.ground_floor * 100}%",
                    "نسبة_البناء_للأدوار_المتكررة": f"{ratios.repeated_floors * 100}%",
                    "نسبة_البناء_للملحق_العلوي": f"{ratios.top_floor * 100}%",
                    "الطوابق_المقترحة": f"{floors}",
                    "مساحة_البناء_الفعالة_للدور_الأرضي": f"{land_area} * {ratios.ground_floor} = {self.format_number(ground_floor_area)} متر مربع",
                    "مساحة_البناء_الفعالة_للمتكرر": f"{land_area} * {ratios.repeated_floors} = {self.format_number(repeated_floors_area)} متر مربع",
                    "مساحة_البناء_الفعالة_للملحق_العلوي": f"{self.format_number(repeated_floors_area)} * {ratios.top_floor} = {self.format_number(top_floor_area)} متر مربع",
                    "مساحة_البناء_الفعالة_للأدوار_المتكررة": f"{self.format_number(repeated_floors_area)} * ({floors} - 2) = {self.format_number(repeated_floors_area)} متر مربع",
                    "نتيجة_مساحة_البناء_الفعالة": f"{self.format_number(ground_floor_area)} + {self.format_number(repeated_floors_area)} + {self.format_number(top_floor_area)} = {self.format_number(total_area)} متر مربع",
                    "معامل_البناء": f"{self.format_number(total_area)} / {self.format_number(land_area)} = {total_area/land_area:.2f}",
                    "نتيجة_معامل_البناء": f"{total_area/land_area:.2f}",
                    "أدوار_الوحدات_التجارية": "دور واحد (الدور الأرضي)",
                    "أدوار_الوحدات_السكنية": f"{floors} - 1 = {floors-1}",
                    "مجموع_المساحة_التجارية": f"{self.format_number(total_commercial_area)} متر مربع",
                    "مجموع_المساحة_السكنية": f"{self.format_number(total_residential_area)} متر مربع",
                    "نطاق_حجم_الوحدات-السكنية": "'80 متر مربع إلى 120 متر مربع'",
                    "الوحدات_السكنية_المقترحة": f"{self.format_number(total_residential_area)} / 100 = {total_residential_area/100:.1f} وحدة سكنية",
                    "نتيجة_الوحدات_السكنية_المقترحة": f"{int(total_residential_area/100)} وحدة سكنية",
                    "نطاق_حجم_الوحدات-التجارية": "'60 متر مربع إلى 100 متر مربع'",
                    "الوحدات_التجارية_المقترحة": f"{self.format_number(total_commercial_area)} / 80 = {total_commercial_area/80:.4f} وحدة تجارية",
                    "نتيجة_الوحدات_التجارية_المقترحة": f"{int(total_commercial_area/80)} وحدة تجارية"
                },
                "توقعات_التمويل": {
                    "تكلفة_شراء_الأرض": {
                        "تكلفة_الشراء_لكل_متر_مربع": f"{self.format_number(land_price_per_sqm)} ريال سعودي",
                        "التكلفة_الكلية": f"{self.format_number(land_area)} * {self.format_number(land_price_per_sqm)} = {self.format_number(total_land_cost)} ريال سعودي",
                        "نتيجة_التكلفة_الكلية": f"{self.format_number(total_land_cost)} ريال سعودي"
                    },
                    "تكاليف_البناء": {
                        "تكلفة_البناء_لكل_متر_مربع": f"{self.format_number(construction_cost_per_sqm)} ريال سعودي",
                        "مجموع_تكاليف_البناء": f"{self.format_number(total_area)} * {construction_cost_per_sqm} = {self.format_number(total_construction_cost)} ريال سعودي",
                        "التكاليف_الإضافية": {
                            "تصميم_معماري": f"{self.format_number(design_cost)} ريال سعودي",
                            "قانوني_وإداري": f"{self.format_number(legal_cost)} ريال سعودي",
                            "تنسيق_الموقع": f"{self.format_number(landscaping_cost)} ريال سعودي"
                        },
                        "المجموع": f"{self.format_number(total_construction_cost)} + {self.format_number(design_cost)} + {self.format_number(legal_cost)} + {self.format_number(landscaping_cost)} = {self.format_number(total_construction_with_additional)} ريال سعودي",
                        "نتيجة_المجموع": f"{self.format_number(total_construction_with_additional)} ريال سعودي"
                    },
                    "الاستثمار_الكلي": f"{self.format_number(total_land_cost)} + {self.format_number(total_construction_with_additional)} = {self.format_number(total_investment)} ريال سعودي",
                    "نتيجة_الاستثمار_الكلي": f"{self.format_number(total_investment)} ريال سعودي",
                    "توقعات_الإيرادات_من_البيع": {
                        "سعر_البيع_السكني_لكل_متر_مربع": f"{self.format_number(residential_sale_price_per_sqm)} ريال سعودي",
                        "سعر_البيع_التجاري_لكل_متر_مربع": f"{self.format_number(commercial_sale_price_per_sqm)} ريال سعودي",
                        "إيرادات_محتملة_من_البيع_السكني": f"{self.format_number(total_residential_area)} * {self.format_number(residential_sale_price_per_sqm)} = {self.format_number(residential_sales_revenue)} ريال سعودي",
                        "إيرادات_محتملة_من_البيع_التجاري": f"{self.format_number(total_commercial_area)} * {self.format_number(commercial_sale_price_per_sqm)} = {self.format_number(commercial_sales_revenue)} ريال سعودي",
                        "نتيجة_الإيرادات_المحتملة_من_البيع": f"{self.format_number(residential_sales_revenue)} + {self.format_number(commercial_sales_revenue)} = {self.format_number(total_sales_revenue)} ريال سعودي",
                        "هامش_الربح_الإجمالي": f"{self.format_number(total_sales_revenue)} - {self.format_number(total_investment)} = {self.format_number(gross_profit)} ريال سعودي",
                        "نتيجة_هامش_الربح_الإجمالي": f"{self.format_number(gross_profit)} ريال سعودي",
                        "نسبة_هامش_الربح_الإجمالي": f"({self.format_number(gross_profit)} / {self.format_number(total_investment)}) * 100 = {profit_margin_percentage:.2f}%",
                        "نتيجة_نسبة_هامش_الربح_الإجمالي": f"{profit_margin_percentage:.2f}%"
                    },
                    "توقعات_الإيرادات_من_الإيجار": {
                        "الإيجار_السنوي_المتوقع_للسكني_لكل_متر_مربع": f"{self.format_number(residential_rent_per_sqm)} ريال سعودي",
                        "الإيجار_السنوي_المتوقع_للتجاري_لكل_متر_مربع": f"{self.format_number(commercial_rent_per_sqm)} ريال سعودي",
                        "الإيجار_السنوي_الكلي_للسكني": f"{self.format_number(total_residential_area)} * {self.format_number(residential_rent_per_sqm)} = {self.format_number(residential_annual_rent)} ريال سعودي",
                        "الإيجار_السنوي_الكلي_للتجاري": f"{self.format_number(total_commercial_area)} * {self.format_number(commercial_rent_per_sqm)} = {self.format_number(commercial_annual_rent)} ريال سعودي",
                        "نتيجة_الإيجار_السنوي_الكلي": f"{self.format_number(residential_annual_rent)} + {self.format_number(commercial_annual_rent)} = {self.format_number(total_annual_rent)} ريال سعودي",
                        "النفقات_التشغيلية": f"20% من {self.format_number(total_annual_rent)} = {self.format_number(operating_expenses)} ريال سعودي",
                        "نتيجة_النفقات_التشغيلية": f"{self.format_number(operating_expenses)} ريال سعودي",
                        "صافي_الإيجار_السنوي": f"{self.format_number(total_annual_rent)} - {self.format_number(operating_expenses)} = {self.format_number(net_annual_rent)} ريال سعودي",
                        "نتيجة_صافي_الإيجار_السنوي": f"{self.format_number(net_annual_rent)} ريال سعودي",
                        "عائد_الاستثمار_من_الإيجار": f"({self.format_number(net_annual_rent)} / {self.format_number(total_investment)}) * 100 = {rental_roi:.2f}%",
                        "نتيجة_عائد_الاستثمار_من_الإيجار": f"{rental_roi:.2f}%"
                    }
                },
                "تقييم_المخاطر": {
                    "تقلبات_السوق": "متوسطة - يواجه سوق العقارات في الرياض تقلبات دورية.",
                    "التغييرات_التنظيمية": "مخاطر منخفضة - بيئة تنظيمية مستقرة مع توقعات بتغييرات طفيفة.",
                    "العوامل_الاقتصادية": "عالية - قد تؤثر التنويع الاقتصادي والاستثمار العام بشكل كبير على قيم العقارات."
                },
                "اعتبارات_استراتيجية": {
                    "اتجاهات_السوق": "يشهد سوق العقارات في الرياض حالياً اتجاهاً تصاعدياً، مدعوماً بالإصلاحات الاقتصادية وزيادة الاستثمار الأجنبي.",
                    "توقيت_الاستثمار": "مثالي - تقدم ظروف السوق الحالية والنمو الاقتصادي المتوقع بيئة مواتية لبدء التطوير.",
                    "التوقعات_طويلة_الأمد": "إمكانية تقدير القيمة طويلة الأمد قوية، مما يجعلها استثمارًا جذابًا لكل من العوائد الفورية والمستقبلية."
                },
                "ملخص_تنفيذي": "يمثل التطوير المقترح في حي النرجس استثمارًا استراتيجيًا سليمًا مع استراتيجية إيرادية مزدوجة من خلال المبيعات والإيجارات. تشير التوقعات المالية إلى عائد استثماري صلب مع مخاطر قابلة للإدارة، متماشية مع ديناميكيات السوق الحالية وآفاق النمو المستقبلية. يُوصى ببدء المشروع على الفور للاستفادة من ظروف السوق المواتية.",
                "توصيات": "المضي قدماً في الاستحواذ والتطوير، مع ضمان إدارة صارمة للتكاليف والالتزام بالجداول الزمنية المتوقعة لتعظيم الربحية. يُنصح بمراقبة مستمرة لظروف السوق وإعادة تقييم منتظمة للاتجاهات الاستراتيجية."
            },
            "ملخص_تنفيذي": "يعد المشروع المقترح فرصة استثمارية جذابة تمزج بين العوائد المالية العالية في القطاع السكني والتجاري، مع التحكم في المخاطر من خلال تحليل دقيق للأسواق. تبين الدراسة الجدوى الاقتصادية لهذا المشروع ومدة استرداد رأس المال المتوقعة."
        }


    def calculate_admin_building_analysis(self, land_area: float, location: str) -> dict:
        # ... (paste the entire calculate_admin_building_analysis method here)
        # Initialize variables
        floors = 4  # عدد الطوابق المقترح
        ratios = AdminBuildingRatios(floors)
        
        # Calculate building areas
        ground_floor_area = land_area * ratios.ground_floor
        first_floor_area = land_area * ratios.first_floor
        repeated_floors_area = first_floor_area * (floors - 2)  # للطوابق المتكررة
        top_floor_area = first_floor_area * ratios.top_floor
        
        # Calculate total area
        total_building_area = ground_floor_area + repeated_floors_area + top_floor_area
        
        # Calculate office units
        avg_office_size = 150  # متوسط مساحة المكتب
        total_offices = int(total_building_area / avg_office_size)

        return {
            "مقدمة": f"دراسة جدوى استثمارية لمشروع مبنى إداري في {location}",
            "العنوان": f"مشروع تطوير مبنى إداري في {location}",
            "تقرير_تحليل_الاستثمار": {
                "مقدمة": f"هذا التحليل الاستثماري المفصل يقيم جدوى وربحية تطوير مشروع مبنى إداري في {location} بالرياض. يشمل التحليل استراتيجيات البيع والإيجار، مع النظر في ديناميكيات السوق الحالية وتقديرات التكاليف والإمكانيات الإيرادية.",
                "تفاصيل_المشروع": {
                    "الموقع": f"{location}، الرياض",
                    "مساحة_الأرض_الإجمالية": f"{self.format_number(land_area)} متر مربع",
                    "نوع_المشروع": "تطوير مبنى إداري",
                    "تنظيمات_التخطيط": f"يسمح ببناء حتى {floors} طوابق"
                },
                                "معايير_التطوير": {
                    "نسبة_البناء_للدور_الأرضي": f"{ratios.ground_floor:.2f}",
                    "نسبة_البناء_للأدوار_المتكررة": f"{ratios.first_floor:.2f}",
                    "نسبة_البناء_للملحق_العلوي": f"{ratios.top_floor:.2f}",
                    "الطوابق_المقترحة": f"{floors}",
                    "مساحة_البناء_الفعالة_للدور_الأرضي": f"مساحة_الأرض_الإجمالية * نسبة_البناء_للدور_الأرضي: {self.format_number(land_area)} * {ratios.ground_floor:.2f} = {self.format_number(ground_floor_area)} متر مربع",
                    "مساحة_البناء_الفعالة_للمتكرر": f"مساحة_الأرض_الإجمالية * نسبة_البناء_للأدوار_المتكررة: {self.format_number(land_area)} * {ratios.first_floor:.2f} = {self.format_number(first_floor_area)} متر مربع",
                    "مساحة_البناء_الفعالة_للملحق_العلوي": f"مساحة_البناء_الفعالة_للمتكرر * نسبة_البناء_للملحق_العلوي: {self.format_number(first_floor_area)} * {ratios.top_floor:.2f} = {self.format_number(top_floor_area)} متر مربع",
                    "مساحة_البناء_الفعالة_للأدوار_المتكررة": f"مساحة_البناء_الفعالة_للمتكرر * (الطوابق_المقترحة - 2): {self.format_number(first_floor_area)} * {floors - 2} = {self.format_number(repeated_floors_area)} متر مربع",
                    "نتيجة_مساحة_البناء_الفعالة": f"مساحة_البناء_الفعالة_للدور_الأرضي + مساحة_البناء_الفعالة_للأدوار_المتكررة + مساحة_البناء_الفعالة_للملحق_العلوي = {self.format_number(ground_floor_area)} + {self.format_number(repeated_floors_area)} + {self.format_number(top_floor_area)} = {self.format_number(total_building_area)} متر مربع",
                    "معامل_البناء": f"نتيجة_مساحة_البناء_الفعالة / مساحة_الأرض_الإجمالية: {self.format_number(total_building_area)} / {self.format_number(land_area)} = {total_building_area/land_area:.2f}",
                    "نتيجة_معامل_البناء": f"{total_building_area/land_area:.2f}",
                    "نطاق_حجم_الوحدات_الإدارية": "100 إلى 200 متر مربع",
                    "الوحدات_الإدارية_المقترحة": f"نتيجة_مساحة_البناء_الفعالة / متوسط_مساحة_الوحدة: {self.format_number(total_building_area)} / {avg_office_size} = {total_offices}",
                    "نتيجة_الوحدات_الإدارية_المقترحة": f"{total_offices} وحدة إدارية"
                },
                "توقعات_التمويل": {
                    "تكلفة_شراء_الأرض": {
                        "تكلفة_الشراء_لكل_متر_مربع": f"{self.format_number(self.location_prices[location])} ريال سعودي",
                        "التكلفة_الكلية": f"مساحة_الأرض_الإجمالية * تكلفة_الشراء_لكل_متر_مربع = {self.format_number(land_area)} * {self.format_number(self.location_prices[location])}",
                        "نتيجة_التكلفة_الكلية": f"{self.format_number(land_area * self.location_prices[location])} ريال سعودي"
                    },
                    "تكاليف_البناء": {
                        "تكلفة_البناء_لكل_متر_مربع": "1,400 ريال سعودي",
                        "مجموع_تكاليف_البناء": f"نتيجة_مساحة_البناء_الفعالة * تكلفة_البناء_لكل_متر_مربع = {self.format_number(total_building_area)} * 1,400",
                        "نتيجة_مجموع_تكاليف_البناء": f"{self.format_number(total_building_area * 1400)} ريال سعودي",
                        "التكاليف_الإضافية": {
                            "تصميم_معماري": "200,000 ريال سعودي",
                            "قانوني_وإداري": "150,000 ريال سعودي",
                            "تنسيق_الموقع": "100,000 ريال سعودي"
                        },
                        "مجموع_التكاليف_الإضافية": "450,000 ريال سعودي",
                        "المجموع": f"مجموع_تكاليف_البناء + مجموع_التكاليف_الإضافية = {self.format_number(total_building_area * 1400)} + 450,000",
                        "نتيجة_المجموع": f"{self.format_number(total_building_area * 1400 + 450000)} ريال سعودي"
                    },
                                        "الاستثمار_الكلي": f"تكلفة_شراء_الأرض + مجموع_تكاليف_البناء = {self.format_number(land_area * self.location_prices[location])} + {self.format_number(total_building_area * 1400 + 450000)}",
                    "نتيجة_الاستثمار_الكلي": f"{self.format_number(land_area * self.location_prices[location] + total_building_area * 1400 + 450000)} ريال سعودي",
                    "توقعات_الإيرادات_من_البيع": {
                        "سعر_البيع_لكل_متر_مربع": f"{self.format_number(self.location_prices[location] * 1.4)} ريال سعودي",
                        "إيرادات_محتملة_من_البيع": f"نتيجة_مساحة_البناء_الفعالة * سعر_البيع_لكل_متر_مربع = {self.format_number(total_building_area)} * {self.format_number(self.location_prices[location] * 1.4)}",
                        "نتيجة_الإيرادات_المحتملة_من_البيع": f"{self.format_number(total_building_area * self.location_prices[location] * 1.4)} ريال سعودي",
                        "هامش_الربح_الإجمالي": f"إيرادات_محتملة_من_البيع - الاستثمار_الكلي = {self.format_number(total_building_area * self.location_prices[location] * 1.4)} - {self.format_number(land_area * self.location_prices[location] + total_building_area * 1400 + 450000)}",
                        "نتيجة_هامش_الربح_الإجمالي": f"{self.format_number(total_building_area * self.location_prices[location] * 1.4 - (land_area * self.location_prices[location] + total_building_area * 1400 + 450000))} ريال سعودي",
                        "نسبة_هامش_الربح_الإجمالي": f"{((total_building_area * self.location_prices[location] * 1.4 - (land_area * self.location_prices[location] + total_building_area * 1400 + 450000)) / (land_area * self.location_prices[location] + total_building_area * 1400 + 450000)) * 100:.2f}%"
                    },
                    "توقعات_الإيرادات_من_الإيجار": {
                        "الإيجار_السنوي_المتوقع_لكل_متر_مربع": f"{self.format_number(self.location_prices[location] * 0.18)} ريال سعودي",
                        "الإيجار_السنوي_الكلي": f"نتيجة_مساحة_البناء_الفعالة * الإيجار_السنوي_المتوقع_لكل_متر_مربع = {self.format_number(total_building_area)} * {self.format_number(self.location_prices[location] * 0.18)}",
                        "نتيجة_الإيجار_السنوي_الكلي": f"{self.format_number(total_building_area * self.location_prices[location] * 0.18)} ريال سعودي",
                        "النفقات_التشغيلية": f"20% من الإيجار_السنوي_الكلي = 0.20 * {self.format_number(total_building_area * self.location_prices[location] * 0.18)}",
                        "نتيجة_النفقات_التشغيلية": f"{self.format_number(total_building_area * self.location_prices[location] * 0.18 * 0.20)} ريال سعودي",
                        "صافي_الإيجار_السنوي": f"الإيجار_السنوي_الكلي - النفقات_التشغيلية = {self.format_number(total_building_area * self.location_prices[location] * 0.18)} - {self.format_number(total_building_area * self.location_prices[location] * 0.18 * 0.20)}",
                        "نتيجة_صافي_الإيجار_السنوي": f"{self.format_number(total_building_area * self.location_prices[location] * 0.18 * 0.80)} ريال سعودي",
                        "عائد_الاستثمار_من_الإيجار": f"صافي_الإيجار_السنوي / الاستثمار_الكلي * 100 = {self.format_number(total_building_area * self.location_prices[location] * 0.18 * 0.80)} / {self.format_number(land_area * self.location_prices[location] + total_building_area * 1400 + 450000)} * 100",
                        "نتيجة_عائد_الاستثمار_من_الإيجار": f"{(total_building_area * self.location_prices[location] * 0.18 * 0.80 / (land_area * self.location_prices[location] + total_building_area * 1400 + 450000)) * 100:.2f}%"
                    }
                },
                "تقييم_المخاطر": {
                    "تقلبات_السوق": "متوسطة - يواجه سوق العقارات التجارية في الرياض تقلبات دورية.",
                    "التغييرات_التنظيمية": "مخاطر منخفضة - بيئة تنظيمية مستقرة مع توقعات بتغييرات طفيفة.",
                    "العوامل_الاقتصادية": "عالية - قد تؤثر التنويع الاقتصادي والاستثمار العام بشكل كبير على قيم العقارات التجارية."
                },
                "اعتبارات_استراتيجية": {
                    "اتجاهات_السوق": "يشهد سوق العقارات التجارية في الرياض حالياً اتجاهاً تصاعدياً، مدعوماً بالإصلاحات الاقتصادية وزيادة الاستثمار الأجنبي.",
                    "توقيت_الاستثمار": "مثالي - تقدم ظروف السوق الحالية والنمو الاقتصادي المتوقع بيئة مواتية لبدء التطوير.",
                    "التوقعات_طويلة_الأمد": "إمكانية تقدير القيمة طويلة الأمد قوية، مع توقعات نمو في الطلب على المساحات المكتبية."
                },
                "ملخص_تنفيذي": f"يمثل التطوير المقترح في {location} استثمارًا استراتيجيًا في سوق المكاتب المتنامي. يوفر المشروع {total_offices} وحدة إدارية بمساحات مرنة تلبي احتياجات السوق.",
                "توصيات": "المضي قدماً في التطوير مع التركيز على جودة التشطيبات والمرافق لتحقيق أعلى عائد ممكن من الإيجارات."
            },
            "ملخص_تنفيذي": f"مشروع تطوير مبنى إداري في {location} يقدم {total_offices} وحدة إدارية عصرية مع توقعات عوائد جذابة من الإيجار والبيع"
        }

if __name__ == "__main__":
    calculator = UnifiedCalculator()
# Add this line

    test_cases = [
        {
            "type": ProjectType.SHOPPING_MALL,
            "params": {
                "land_area": 10000,
                "location": "حي النرجس",
                "floors": 3
            }
        },
        {
            "type": ProjectType.RESIDENTIAL,
            "params": {
                "land_area": 3500,
                "location": "حي النرجس",
                "floors": 4
            }
        },
        {
            "type": ProjectType.COMMERCIAL,
            "params": {
                "land_area": 3000,
                "location": "حي النرجس",
                "floors": 4
            }
        },
        {
            "type": ProjectType.MIXED_USE,
            "params": {
                "land_area": 5000,
                "location": "حي النرجس",
                "floors": 6
            }
        },
        {
            "type": ProjectType.VILLA,
            "params": {
                "land_area": 2000,
                "location": "حي النرجس"
            }
        },
        {
            "type": ProjectType.SINGLE_VILLA,
            "params": {
                "land_area": 500,
                "location": "حي النرجس"
            }
        },
        {
            "type": ProjectType.RESIDENTIAL_COMPOUND,  # Add this test case
            "params": {
                "land_area": 5000,
                "location": "حي النرجس",
                "effective_land_ratio": 0.40
            }
        },
        {
            "type": ProjectType.ADMIN_BUILDING,  # Add this test case
            "params": {
                "land_area": 2000,
                "location": "حي النرجس"
            }
        }
    ]

    print("تحليل الاستثمارات العقارية:\n")
    
    for case in test_cases:
        print(f"\nمشروع {case['type'].value}:")
        print("-" * 50)
        
        result = None
        if case['type'] == ProjectType.SINGLE_VILLA:
            result = calculator.calculate_villa_analysis(**case['params'])
        elif case['type'] == ProjectType.VILLA:
            result = calculator.calculate_villa_context(**case['params'])
        elif case['type'] == ProjectType.RESIDENTIAL_COMPOUND:
            result = calculator.calculate_compound_analysis(**case['params'])
        elif case['type'] == ProjectType.ADMIN_BUILDING:
            result = calculator.calculate_admin_building_analysis(**case['params'])
        elif case['type'] == ProjectType.SHOPPING_MALL:
            result = calculator.calculate_mall_context(**case['params'])
        elif case['type'] == ProjectType.RESIDENTIAL:
            result = calculator.calculate_residential_context(**case['params'])
        elif case['type'] == ProjectType.COMMERCIAL:
            result = calculator.calculate_commercial_context(**case['params'])
        else:  # MIXED_USE
            result = calculator.calculate_mixed_use_context(**case['params'])

        print(json.dumps(result, ensure_ascii=False, indent=2))
        print("-" * 50)