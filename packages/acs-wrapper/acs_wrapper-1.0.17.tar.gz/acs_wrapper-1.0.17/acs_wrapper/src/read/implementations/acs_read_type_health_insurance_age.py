__author__ = 'diegopinheiro'
__email__ = 'diegompin@gmail.com'
__github__ = 'https://github.com/diegompin'

from acs_wrapper.src.read.acs_read_base import AcsRead


class AcsReadTypeHealthInsuranceAge(AcsRead):

    def __init__(self, datapath):
        super().__init__(datapath=datapath, prefix='INSURANCECOREVAGE', datafile='B27010',
                         column_format='HD01_VD%02d', is_percent=False)

    def get_mappings(self):
        '''
        HD01_VD01
        Estimate; Total:

        HD01_VD04
        Estimate; Under 19 years:
        - With one type of health insurance coverage:
        - With employer-based health insurance only

        HD01_VD05
        Estimate; Under 19 years:
        - With one type of health insurance coverage:
        - With direct-purchase health insurance only

        HD01_VD06
        Estimate; Under 19 years:
        - With one type of health insurance coverage:
        - With Medicare coverage only

        HD01_VD07
        Estimate; Under 19 years:
        - With one type of health insurance coverage:
        - With Medicaid/means-tested public coverage only

        HD01_VD08
        Estimate; Under 19 years:
        - With one type of health insurance coverage:
        - With TRICARE/military health coverage only

        HD01_VD09
        Estimate; Under 19 years:
        - With one type of health insurance coverage:
        - With VA Health Care only

        HD01_VD11
        Estimate; Under 19 years:
        - With two or more types of health insurance coverage:
        - With employer-based and direct-purchase coverage

        HD01_VD12
        Estimate; Under 19 years:
        - With two or more types of health insurance coverage:
        - With employer-based and Medicare coverage

        HD01_VD13
        Estimate; Under 19 years:
        - With two or more types of health insurance coverage:
        - With Medicare and Medicaid/means-tested public coverage

        HD01_VD14
        Estimate; Under 19 years:
        - With two or more types of health insurance coverage:
        - Other private only combinations

        HD01_VD15
        Estimate; Under 19 years:
        - With two or more types of health insurance coverage:
        - Other public only combinations

        HD01_VD16
        Estimate; Under 19 years:
        - With two or more types of health insurance coverage:
        - Other coverage combinations

        HD01_VD17
        Estimate; Under 19 years:
        - No health insurance coverage

        HD01_VD20
        Estimate; 19 to 34 years:
        - With one type of health insurance coverage:
        - With employer-based health insurance only

        HD01_VD21
        Estimate; 19 to 34 years:
        - With one type of health insurance coverage:
        - With direct-purchase health insurance only

        HD01_VD22
        Estimate; 19 to 34 years:
        - With one type of health insurance coverage:
        - With Medicare coverage only

        HD01_VD23
        Estimate; 19 to 34 years:
        - With one type of health insurance coverage:
        - With Medicaid/means-tested public coverage only

        HD01_VD24
        Estimate; 19 to 34 years:
        - With one type of health insurance coverage:
        - With TRICARE/military health coverage only

        HD01_VD25
        Estimate; 19 to 34 years:
        - With one type of health insurance coverage:
        - With VA Health Care only

        HD01_VD27
        Estimate; 19 to 34 years:
        - With two or more types of health insurance coverage:
        - With employer-based and direct-purchase coverage

        HD01_VD28
        Estimate; 19 to 34 years:
        - With two or more types of health insurance coverage:
        - With employer-based and Medicare coverage

        HD01_VD29
        Estimate; 19 to 34 years:
        - With two or more types of health insurance coverage:
        - With Medicare and Medicaid/means-tested public coverage

        HD01_VD30
        Estimate; 19 to 34 years:
        - With two or more types of health insurance coverage:
        - Other private only combinations

        HD01_VD31
        Estimate; 19 to 34 years:
        - With two or more types of health insurance coverage:
        - Other public only combinations

        HD01_VD32
        Estimate; 19 to 34 years:
        - With two or more types of health insurance coverage:
        - Other coverage combinations

        HD01_VD33
        Estimate; 19 to 34 years:
        - No health insurance coverage

        HD01_VD36
        Estimate; 35 to 64 years:
        - With one type of health insurance coverage:
        - With employer-based health insurance only

        HD01_VD37
        Estimate; 35 to 64 years:
        - With one type of health insurance coverage:
        - With direct-purchase health insurance only

        HD01_VD38
        Estimate; 35 to 64 years:
         With one type of health insurance coverage:
         - With Medicare coverage only

        HD01_VD39
        Estimate; 35 to 64 years:
        - With one type of health insurance coverage:
        - With Medicaid/means-tested public coverage only

        HD01_VD40
        Estimate; 35 to 64 years:
        - With one type of health insurance coverage:
        - With TRICARE/military health coverage only

        HD01_VD41
        Estimate; 35 to 64 years:
        - With one type of health insurance coverage:
        - With VA Health Care only

        HD01_VD43
        Estimate; 35 to 64 years:
        - With two or more types of health insurance coverage:
        - With employer-based and direct-purchase coverage

        HD01_VD44
        Estimate; 35 to 64 years:
        - With two or more types of health insurance coverage:
        - With employer-based and Medicare coverage

        HD01_VD45
        Estimate; 35 to 64 years:
        - With two or more types of health insurance coverage:
        - With direct-purchase and Medicare coverage

        HD01_VD46
        Estimate; 35 to 64 years:
        - With two or more types of health insurance coverage:
        - With Medicare and Medicaid/means-tested public coverage

        HD01_VD47
        Estimate; 35 to 64 years:
        - With two or more types of health insurance coverage:
        - Other private only combinations

        HD01_VD48
        Estimate; 35 to 64 years:
        - With two or more types of health insurance coverage:
        - Other public only combinations

        HD01_VD49
        Estimate; 35 to 64 years:
        - With two or more types of health insurance coverage:
        - Other coverage combinations

        HD01_VD50
        Estimate; 35 to 64 years:
        - No health insurance coverage

        HD01_VD53
        Estimate; 65 years and over:
        - With one type of health insurance coverage:
        - With employer-based health insurance only
        HD01_VD54
        Estimate; 65 years and over:
        - With one type of health insurance coverage:
        - With direct-purchase health insurance only

        HD01_VD55
        Estimate; 65 years and over:
        - With one type of health insurance coverage:
        - With Medicare coverage only

        HD01_VD56
        Estimate; 65 years and over:
        - With one type of health insurance coverage:
        - With TRICARE/military health coverage only

        HD01_VD57
        Estimate; 65 years and over:
        - With one type of health insurance coverage:
        - With VA Health Care only

        HD01_VD59
        Estimate; 65 years and over:
        - With two or more types of health insurance coverage:
        - With employer-based and direct-purchase coverage

        HD01_VD60
        Estimate; 65 years and over:
        - With two or more types of health insurance coverage:
        - With employer-based and Medicare coverage

        HD01_VD61
        Estimate; 65 years and over:
        - With two or more types of health insurance coverage:
        - With direct-purchase and Medicare coverage

        HD01_VD62
        Estimate; 65 years and over:
        - With two or more types of health insurance coverage:
        - With Medicare and Medicaid/means-tested public coverage

        HD01_VD63
        Estimate; 65 years and over:
        - With two or more types of health insurance coverage:
        - Other private only combinations

        HD01_VD64
        Estimate; 65 years and over:
        - With two or more types of health insurance coverage:
        - Other public only combinations

        HD01_VD65
        Estimate; 65 years and over:
        - With two or more types of health insurance coverage:
        - Other coverage combinations

        HD01_VD66
        Estimate; 65 years and over:
        - No health insurance coverage



        '''
        mappings = [
            {
                'TOTAL': [1],
                'EMPLOYER_BASED': [4, 20, 36, 53],
                'DIRECT_PURCHASE': [5, 14, 21, 37, 54],
                'EMPLOYER_BASED_DIRECT_PURCHASE': [11, 27, 43, 59],
                'EMPLOYER_BASED_MEDICARE': [12, 28, 44, 60],
                'DIRECT_PURCHASE_MEDICARE': [45, 61],
                'MEDICARE': [6, 22, 38, 55],
                'MEDICAID': [7, 23, 39],
                'MEDICARE_MEDICAID': [13, 29, 46, 62],
                'TRICARE_MILITARY': [8, 24, 40, 56],
                'VETERAN': [9, 25, 41, 67],
                'OTHER': [14, 15, 16, 30, 31, 32, 47, 48, 49, 63, 64, 65],
                'NO_INSURANCE': [17, 33, 50, 66],

            }
        ]
        return mappings
