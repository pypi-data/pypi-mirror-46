"""Auto-generated file, do not edit by hand. MU metadata"""
from ..phonemetadata import NumberFormat, PhoneNumberDesc, PhoneMetadata

PHONE_METADATA_MU = PhoneMetadata(id='MU', country_code=230, international_prefix='0(?:0|[24-7]0|3[03])',
    general_desc=PhoneNumberDesc(national_number_pattern='(?:[2-468]|5\\d)\\d{6}', possible_length=(7, 8)),
    fixed_line=PhoneNumberDesc(national_number_pattern='(?:2(?:[03478]\\d|1[0-7]|6[0-79])|4(?:[013568]\\d|2[4-7])|54(?:4\\d|71)|6\\d\\d|8(?:14|3[129]))\\d{4}', example_number='54480123', possible_length=(7, 8)),
    mobile=PhoneNumberDesc(national_number_pattern='5(?:4(?:2[1-389]|7[1-9])|87[15-8])\\d{4}|5(?:2[589]|4[489]|7\\d|8[0-689]|9[0-8])\\d{5}', example_number='52512345', possible_length=(8,)),
    toll_free=PhoneNumberDesc(national_number_pattern='80[0-2]\\d{4}', example_number='8001234', possible_length=(7,)),
    premium_rate=PhoneNumberDesc(national_number_pattern='30\\d{5}', example_number='3012345', possible_length=(7,)),
    voip=PhoneNumberDesc(national_number_pattern='3(?:20|9\\d)\\d{4}', example_number='3201234', possible_length=(7,)),
    preferred_international_prefix='020',
    number_format=[NumberFormat(pattern='(\\d{3})(\\d{4})', format='\\1 \\2', leading_digits_pattern=['[2-46]|8[013]']),
        NumberFormat(pattern='(\\d{4})(\\d{4})', format='\\1 \\2', leading_digits_pattern=['5'])])
