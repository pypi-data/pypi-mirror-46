"""Auto-generated file, do not edit by hand. BG metadata"""
from ..phonemetadata import NumberFormat, PhoneNumberDesc, PhoneMetadata

PHONE_METADATA_BG = PhoneMetadata(id='BG', country_code=359, international_prefix='00',
    general_desc=PhoneNumberDesc(national_number_pattern='[2-7]\\d{6,7}|[89]\\d{6,8}|2\\d{5}', possible_length=(6, 7, 8, 9), possible_length_local_only=(4, 5)),
    fixed_line=PhoneNumberDesc(national_number_pattern='2\\d{5,7}|(?:43[1-6]|70[1-9])\\d{4,5}|(?:[36]\\d|4[124-7]|[57][1-9]|8[1-6]|9[1-7])\\d{5,6}', example_number='2123456', possible_length=(6, 7, 8), possible_length_local_only=(4, 5)),
    mobile=PhoneNumberDesc(national_number_pattern='43[07-9]\\d{5}|(?:48|8[7-9]\\d|9(?:8\\d|9[69]))\\d{6}', example_number='48123456', possible_length=(8, 9)),
    toll_free=PhoneNumberDesc(national_number_pattern='800\\d{5}', example_number='80012345', possible_length=(8,)),
    premium_rate=PhoneNumberDesc(national_number_pattern='90\\d{6}', example_number='90123456', possible_length=(8,)),
    personal_number=PhoneNumberDesc(national_number_pattern='700\\d{5}', example_number='70012345', possible_length=(8,)),
    national_prefix='0',
    national_prefix_for_parsing='0',
    number_format=[NumberFormat(pattern='(\\d{6})', format='\\1', leading_digits_pattern=['1']),
        NumberFormat(pattern='(\\d)(\\d)(\\d{2})(\\d{2})', format='\\1 \\2 \\3 \\4', leading_digits_pattern=['2'], national_prefix_formatting_rule='0\\1'),
        NumberFormat(pattern='(\\d{3})(\\d{4})', format='\\1 \\2', leading_digits_pattern=['43[1-6]|70[1-9]'], national_prefix_formatting_rule='0\\1'),
        NumberFormat(pattern='(\\d)(\\d{3})(\\d{3,4})', format='\\1 \\2 \\3', leading_digits_pattern=['2'], national_prefix_formatting_rule='0\\1'),
        NumberFormat(pattern='(\\d{2})(\\d{3})(\\d{2,3})', format='\\1 \\2 \\3', leading_digits_pattern=['[356]|4[124-7]|7[1-9]|8[1-6]|9[1-7]'], national_prefix_formatting_rule='0\\1'),
        NumberFormat(pattern='(\\d{3})(\\d{2})(\\d{3})', format='\\1 \\2 \\3', leading_digits_pattern=['(?:70|8)0'], national_prefix_formatting_rule='0\\1'),
        NumberFormat(pattern='(\\d{3})(\\d{3})(\\d{2})', format='\\1 \\2 \\3', leading_digits_pattern=['43[1-7]|7'], national_prefix_formatting_rule='0\\1'),
        NumberFormat(pattern='(\\d{2})(\\d{3})(\\d{3,4})', format='\\1 \\2 \\3', leading_digits_pattern=['[48]|9[08]'], national_prefix_formatting_rule='0\\1'),
        NumberFormat(pattern='(\\d{3})(\\d{3})(\\d{3})', format='\\1 \\2 \\3', leading_digits_pattern=['9'], national_prefix_formatting_rule='0\\1')],
    intl_number_format=[NumberFormat(pattern='(\\d)(\\d)(\\d{2})(\\d{2})', format='\\1 \\2 \\3 \\4', leading_digits_pattern=['2']),
        NumberFormat(pattern='(\\d{3})(\\d{4})', format='\\1 \\2', leading_digits_pattern=['43[1-6]|70[1-9]']),
        NumberFormat(pattern='(\\d)(\\d{3})(\\d{3,4})', format='\\1 \\2 \\3', leading_digits_pattern=['2']),
        NumberFormat(pattern='(\\d{2})(\\d{3})(\\d{2,3})', format='\\1 \\2 \\3', leading_digits_pattern=['[356]|4[124-7]|7[1-9]|8[1-6]|9[1-7]']),
        NumberFormat(pattern='(\\d{3})(\\d{2})(\\d{3})', format='\\1 \\2 \\3', leading_digits_pattern=['(?:70|8)0']),
        NumberFormat(pattern='(\\d{3})(\\d{3})(\\d{2})', format='\\1 \\2 \\3', leading_digits_pattern=['43[1-7]|7']),
        NumberFormat(pattern='(\\d{2})(\\d{3})(\\d{3,4})', format='\\1 \\2 \\3', leading_digits_pattern=['[48]|9[08]']),
        NumberFormat(pattern='(\\d{3})(\\d{3})(\\d{3})', format='\\1 \\2 \\3', leading_digits_pattern=['9'])],
    mobile_number_portable_region=True)
