class EnumValue(object):
    def __init__(self,
                 identifier):
        self._identifier = identifier

    @property
    def identifier(self):
        return self._identifier

    def __repr__(self):
        return '<Enum {0}>'.format(self._identifier)

    def __str__(self):
        return '{0}'.format(self._identifier)




class Enum(object):
    def __init__(self, **kwargs):
        self._values = []
        for key, value in list(kwargs.items()):
            enum_value = EnumValue(value)
            setattr(self, key, enum_value)
            self._values.append(enum_value)

    def find(self,
             identifier):
        for  value in self._values:
            if identifier == value.identifier:
                return value
        return None

    def from_id(self,
                identifier):
        if self.find(identifier) is None:
            raise ValueError('Unexpected identifier {0}'.format(identifier))
        else:
            return self.find(identifier)

    def __contains__(self, value):
        return value in self._values

    def __iter__(self):
        return iter(self._values)

class ExtendableEnum(Enum):
    def __init__(self, **kwargs):
        super(ExtendableEnum, self).__init__(**kwargs)
        class Extension(EnumValue):
            def __init__(self,
                         identifier):
                super(Extension, self).__init__(identifier)

            def __eq__(self, other):
                if isinstance(other, self.__class__):
                    return self.identifier == other.identifier
                else:
                    return self.identifier == other

        self._Extension = Extension

    def extend(self, identifier):
        res = super(ExtendableEnum, self).find(identifier)
        if res is None:
            return self._Extension(identifier)
        else :
            return res

    def __contains__(self, value):
        return super(ExtendableEnum, self).__contains__(value) or isinstance(value, self._Extension)

'''
These values defines how FieldDescriptor should behave.
soft - usualy set when value of field were retrieved from responce from server,
       means that FieldDescriptor can return field.value without retrieving data from server
hard - usealy set when value is set by user (ie. doc.title = u'new title'), means
       that FieldDescriptor can return field.value without retrieving data from server.
       Normaly values of fields with hard value status, should not be overwritten by with values
       retrieved from server.
none - value haven't been set yet, means that FieldDescriptor should retrive data from server
       before returning field.value. 'invalidate' method usualy simpli sets status to 'none'.
default - is used for fields which is not attached to 'database_object', means that 'field.value'
       could be returned by FieldDescriptor if field is not attached to any 'database_object'.
       Also fields with 'default' status should not be copied during FieldGroup.hard_set because
       it's not a real value.
'''
ValueStatus = Enum(soft = 'soft',
                   hard = 'hard',
                   none = 'none',
                   default = 'default')

FieldKind = Enum(regular = 'regular',
                 readonly = 'readonly')


DocumentStatus = Enum(published = 'PUBLISHED',
                      new = 'NEW',
                      unpublished = 'UNPUBLISHED',
                      deleted = 'DELETED')


License = Enum(none = 'no',
               book_or_ebook = 'yes',
               book = 'book',
               ebook = 'ebook',
               acquisition = 'acquisition')

AcademicCategory = Enum(bachelor_thesis = 1,
                        diploma_thesis = 2,
                        doctoral_thesis = 3,
                        examination_thesis = 4,
                        research_paper_pre_university = 5,
                        term_paper = 6,
                        thesis_MA = 7,
                        masters_thesis = 8,
                        internship_report_pre_university = 9,
                        internship_report = 10,
                        presentation_essay_pre_university = 11,
                        Presentation_elaboration = 12,
                        lecture_notes = 13,
                        lesson_plan = 14,
                        research_paper = 20,
                        scientific_essay = 15,
                        term_paper_advanced_seminar = 21,
                        elaboration = 16,
                        seminar_paper = 22,
                        essay = 17,
                        scholarly_research_paper = 23,
                        excerpt = 18,
                        presentation_handout = 24,
                        textbook = 19,
                        intermediate_diploma_thesis = 25,
                        intermediate_examination_paper = 26,
                        instruction = 32,
                        scientific_study = 27,
                        literature_review = 28,
                        professorial_dissertation = 34,
                        template_example = 40,
                        exegesis = 35,
                        composition = 41,
                        swiss_diploma_thesis = 36,
                        technical_report = 42,
                        project_report = 37,
                        lecture_notes_ = 43,
                        anthology = 38,
                        academic_paper = 44,
                        classic = 39,
                        written_test = 45,
                        abstract = 46,
                        exam_revision = 47,
                        polemic_paper = 48,
                        submitted_assignment = 49,
                        presentation_slides = 50)


Language = ExtendableEnum(German = 'de',
                          Danish = 'da',
                          English = 'en',
                          French = 'fr',
                          Dutch = 'nl',
                          Italian = 'it',
                          Catalan = 'ca',
                          Croatian = 'hr',
                          Latin = 'la',
                          Norwegian = 'no',
                          Polish = 'pl',
                          Portugues = 'pt',
                          Russian = 'ru',
                          Swedish = 'sv',
                          Serbian = 'sr',
                          Spanish = 'es',
                          Turkish = 'tr',
                          Hungarian = 'hu',
                          Arabic = 'ar',
                          Czech = 'cs',
                          Greek = 'el',
                          Estonian = 'et',
                          Finnish = 'fi',
                          Romanian = 'ro',
                          Icelandic = 'is',
                          Lithuanian = 'lt',
                          Slovakian = 'sk',
                          Slovenian = 'sl',
                          Urdu = 'ur',
                          Mandarin = 'zh',
                          Albanian = 'sq',
                          Afrikaans = 'af',
                          Korean = 'ko',
                          Thai = 'th',
                          Tsonga = 'ts',
                          Bosnian = 'bs',
                          Bulgarian = 'bg',
                          Ukrainian = 'uk',
                          Vietnamese = 'vi',
                          Hebrew = 'he',
                          Japanese = 'ja')


Country = ExtendableEnum(Afghanistan = 'AFG',
                         Albania = 'ALB',
                         Argentina = 'ARG',
                         Australia = 'AUS',
                         Austria = 'AUT',
                         Belarus = 'BLR',
                         Bolivia = 'BOL',
                         Brazil = 'BRA',
                         Canada = 'CAN',
                         Chile = 'CHL',
                         China = 'CHN',
                         Colombia = 'COL',
                         Croatia = 'HRV',
                         Cuba = 'CUB',
                         Cyprus = 'CYP',
                         CzechRepublic = 'CZE',
                         Denmark = 'DNK',
                         Egypt = 'EGY',
                         Estonia = 'EST',
                         Ethiopia = 'ETH',
                         Finland = 'FIN',
                         France = 'FRA',
                         Georgia = 'GEO',
                         Germany = 'DEU',
                         Greece = 'GRC',
                         Hungary = 'HUN',
                         Iceland = 'ISL',
                         India = 'IND',
                         Iran = 'IRN',
                         Iraq = 'IRQ',
                         Ireland = 'IRL',
                         Israel = 'ISR',
                         Italy = 'ITA',
                         Jamaica = 'JAM',
                         Japan = 'JPN',
                         Liechtenstein = 'LIE',
                         Macedonia = 'MKD',
                         Mexico = 'MEX',
                         Moldova = 'MDA',
                         Monaco = 'MCO',
                         Mongolia = 'MNG',
                         Mozambique = 'MOZ',
                         Myanmar = 'MMR',
                         Netherlands = 'NLD',
                         Norway = 'NOR',
                         Poland = 'POL',
                         Portugal = 'PRT',
                         Romania = 'ROU',
                         Russia = 'RUS',
                         Serbia = 'SRB',
                         Slovakia = 'SVK',
                         Slovenia = 'SVN',
                         Somalia = 'SOM',
                         Spain = 'ESP',
                         Sweden = 'SWE',
                         Switzerland = 'CHE',
                         Syria = 'SYR',
                         Thailand = 'THA',
                         Turkey = 'TUR',
                         Ukraine = 'UKR',
                         UnitedKingdom = 'GBR',
                         USA = 'USA',
                         Belgium = 'BEL',
                         Bulgaria = 'BGR',
                         CostaRica = 'CRI',
                         DominicanRepublic = 'DOM',
                         Ecuador = 'ECU',
                         ElSalvador = 'SLV',
                         Guatemala = 'GTM',
                         Honduras = 'HND',
                         Latvia = 'LVA',
                         Lithuania = 'LTU',
                         Luxembourg = 'LUX',
                         Malta = 'MLT',
                         NewZealand = 'NZL',
                         Nicaragua = 'NIC',
                         Panama = 'PAN',
                         Paraguay = 'PRY',
                         Peru = 'PER',
                         Venezuela = 'VEN')

VLBCategory = ExtendableEnum(philosophy = 520,
                             psychology = 530,
                             history = 550,
                             education = 570,
                             chemistry = 650,
                             earth_sciences = 660,
                             art = 580,
                             music = 590,
                             biology = 670,
                             mathematics = 620,
                             technology = 680,
                             fiction = 111,
                             computer_science = 630,
                             economy = 780,
                             medicine = 690,
                             social_sciences = 710,
                             sociology = 720,
                             political_science = 730,
                             anthropology = 750,
                             guide = 310)


ContributorRole = ExtendableEnum(author = 'A01',
                                 composer = 'A06',
                                 artist = 'A07',
                                 photographer = 'A08',
                                 actor = 'E01',
                                 dancer  = 'E02')


# see codelist 38 ( documentation/onix/3.0/codelists/onix-codelist-38.htm )
MediaFileTypeCode = Enum(whole_product = 1,
                         application_software_demo = 2,
                         image_whole_cover = 3,
                         image_front_cover = 4,
                         image_whole_cover_high_quality = 5,
                         image_front_cover_high_quality = 6,
                         image_front_cover_thumbnail = 7,
                         image_contributors = 8,
                         image_for_series = 10,
                         image_series_logo = 11,
                         image_product_logo = 12,
                         image_Master_brand_logo = 16,
                         image_publisher_logo = 17,
                         image_imprint_logo = 18,
                         image_table_of_contents = 22,
                         image_sample_content = 23,
                         image_back_cover = 24,
                         image_back_cover_high_quality = 25,
                         image_back_cover_thumbnail = 26,
                         image_other_cover_material = 27,
                         image_promotional_material = 28,
                         video_segment_unspecified = 29,
                         audio_segment_unspecified = 30,
                         video_author_presentation_commentary = 31,
                         video_author_interview = 32,
                         video_author_reading = 33,
                         video_cover_material = 34,
                         video_sample_content = 35,
                         video_promotional_material = 36,
                         video_review = 37,
                         video_other_commentary_discussion = 38,
                         audio_author_presentation_commentary = 41,
                         audio_author_interview = 42,
                         audio_author_reading = 43,
                         audio_sample_content = 44,
                         audio_promotional_material = 45,
                         audio_review = 46,
                         audio_other_commentary_discussion = 47,
                         application_sample_content = 51,
                         application_promotional_material = 52)


# see codelist 39 ( documentation/onix/3.0/codelists/onix-codelist-39.htm )
MediaFileFormatCode = Enum(gif=2,
                           jpg=3,
                           pdf=4,
                           tif = 5,
                           realaudio = 6,
                           mp3  = 7,
                           mpeg4 = 8,
                           png = 9,
                           wma = 10,
                           aac = 11,
                           wav = 12,
                           aiff = 13,
                           wmv = 14,
                           ogg = 15,
                           avi = 16,
                           mov = 17,
                           flash=18,
                           video3gp = 19,
                           webm = 20)


# see codelist 40 ( documentation/onix/3.0/codelists/onix-codelist-40.htm )
MediaFileLinkTypeCode = Enum(url = 1,
                             doi = 2,
                             purl = 3,
                             urn = 4,
                             ftp = 5,
                             filename = 5)


BisacCode = ExtendableEnum(architecture= 'ARC000000',
                           art = 'ART000000',
                           computers = 'COM000000',
                           cooking= 'CKB000000',
                           drama = 'DRA000000',
                           education = 'EDU000000',
                           fiction= 'FIC000000',
                           games = 'GAM000000',
                           gardening = 'GAR000000',
                           history= 'HIS000000',
                           humor = 'HUM000000',
                           law = 'LAW000000',
                           mathematics = 'MAT000000',
                           medical= 'MED000000',
                           music = 'MUS000000',
                           nature = 'NAT000000',
                           pets = 'PET000000',
                           philosophy = 'PHI000000',
                           psychology = 'PSY000000',
                           religion = 'REL000000',
                           science= 'SCI000000',
                           technology = 'TEC000000',
                           transportation = 'TRA000000',
                           travel = 'TRV000000')

ThemaCode = ExtendableEnum()

FileType = Enum(ebook_pdf = 'ebook_pdf',
                ebook_epub = 'ebook_epub',
                ebook_mobi = 'ebook_mobi',
                ebook_ibooks = 'ebook_ibooks',
                pod_pdf = 'pod_pdf',
                audiobook = 'audiobook',
                software = 'software',
                cover_pod_pdf_final = 'cover_pod_pdf_final',
                cover_marketing_jpg = 'cover_marketing_jpg',
                other = 'other')

PriceType = Enum(auto = 'AUTO',
                 open_access = 'OPEN_ACCESS',
                 no_price = 'NO_PRICE',
                 manual = 'MANUAL')

CatalogType = Enum(academic = 'academic',
                   non_academic = 'non_academic')


EBookFileType = Enum(pdf = 'pdf',
                     epub = 'epub',
                     mobi = 'mobi',
                     ibooks = 'ibooks')

PreviewFileType = Enum(pdf= 'pdf',
                    html = 'html')

IsbnType = Enum(book = 'book',
                epub = 'ebook::epub',
                mobi = 'ebook::mobi',
                ibooks = 'ebook::ibooks',
                pdf = 'ebook::pdf',
                audiobook = 'audiobook',
                software = 'software',
                ebook = 'ebook')

EventTarget = Enum(book = 'book',
                   cover = 'cover',
                   document = 'document',
                   ebook = 'ebook',
                   epub = 'epub',
                   mobi = 'mobi',
                   ibooks = 'ibooks',
                   audiobook = 'audiobook',
                   software = 'software',
                   raw_document = 'raw-document',
                   vlb_onix = 'vlb-onix',
                   preview = 'preview',
                   account = 'account',
                   order = 'order',
                   user = 'user',
                   payment = 'payment',
                   extract = 'extract',
                   screenshot = 'screenshot')

EventAction = Enum(price_changed = 'price-changed',
                   created = 'created',
                   uploaded = 'uploaded',
                   changed = 'changed',
                   blocked = 'blocked',
                   deleted = 'deleted',
                   publication_availability_changed = 'publication-availability-changed',
                   published = 'published',
                   unpublished = 'unpublished',
                   creation = 'creation',
                   subscribed = 'subscribed',
                   unsubscribed = 'unsubscribed',
                   distribution = 'distribution',
                   cover_created_book = 'cover-created-book',
                   cover_created_ebook = 'cover-created-ebook',
                   cover_created_epub = 'cover-created-epub',
                   cover_created_distribution = 'cover-created-distribution',
                   refresh = 'refresh',
                   unblocked = 'unblocked',
                   purchased = 'purchased',
                   payment_changed = 'payment-changed',
                   fulfillment_changed = 'fulfillment-changed',
                   full_manually_requested = 'full-manually-requested',
                   metadata_manually_requested = 'metadata-manually-requested')

EventType = Enum(metadata = 'metadata',
                 conversion = 'conversion',
                 rawdata = 'rawdata',
                 publication = 'publication',
                 distribution = 'distribution',
                 info_mail = 'info-mail',
                 uploaded = 'uploaded',
                 configuration = 'configuration',
                 accounting = 'accounting',
                 preview = 'preview',
                 entry = 'entry')

EventResult = Enum(ok = 'OK',
                   error = 'ERR')

UserStatus = Enum(active = 'ACTIVE',
                  deleted = 'DELETED')

Gender = Enum(male = 'M',
              female = 'F',
              unknown = 'NULL')

Subscription = Enum(author = 'author',
                    buyer = 'buyer',
                    general = 'general')

PublicationType = Enum(pdf = 'pdf',
                       epub = 'epub',
                       mobi = 'mobi',
                       ibooks = 'ibooks',
                       audiobook = 'audiobook',
                       software = 'software',
                       pod = 'pod')

TaxType = Enum(vat_percentage = 'vat_percentage',
               eu_reverse_charge = 'eu_reverse_charge',
               no_tax = 'no_tax')

OnixStyle = Enum(amazon = 'amazon',
                 google = 'google',
                 vlb = 'vlb',
                 tolino = 'tolino',
                 skoobe = 'skoobe',
                 knv = 'knv',
                 international = 'international',
                 ceebo = 'ceebo',
                 ciando = 'ciando',
                 beam = 'beam',
                 libri = 'libri',
                 schweitzer = 'schweitzer',
                 rdw = 'rdw',
                 olf = 'olf',
                 audible = 'audible',
                 bicmedia = 'bicmedia',
                 bookwire = 'bookwire',
                 divibib = 'divibib',
                 doccheck = 'doccheck',
                 genios = 'genios',
                 kobo = 'kobo',
                 lernando = 'lernando',
                 nexway = 'nexway',
                 parkteam = 'parkteam',
                 pubdatanet = 'pubdatanet',
                 softdist = 'softdist',
                 steinsche = 'steinsche',
                 tigerbooks = 'tigerbooks',
                 mojoreads = 'mojoreads',
                 amzprint = 'amzprint',
                 wlb = 'wlb',
                 default = 'default')

OnixType = Enum(short = 'short',
                reference = 'reference')


OnixStatus = Enum(current = 'current',
                  available = 'available',
                  unavailable = 'unavailable',
                  deleted = 'deleted',
                  blocked = 'blocked')


AdultFlag = Enum(unrated = 'UNRATED',
                 any_adult_audience = 'ANY_ADULT_AUDIENCE',
                 content_warning = 'CONTENT_WARNING',
                 content_warning_sex = 'CONTENT_WARNING_SEX',
                 content_warning_violence = 'CONTENT_WARNING_VIOLENCE',
                 content_warning_drug_taking = 'CONTENT_WARNING_DRUG_TAKING',
                 content_warning_language = 'CONTENT_WARNING_LANGUAGE',
                 content_warning_intolerance = 'CONTENT_WARNING_INTOLERANCE')

ChildrenFlag = Enum(unrated = 'UNRATED',
                    children_juvenile = 'CHILDREN_JUVENILE')

ProvisionRuleAlgorithm = Enum(percentage = 'PERCENTAGE',
                              fixed = 'FIXED',
                              progression = 'PROGRESSION',
                              fee = 'FEE',
                              inter_realm = 'INTER_REALM',
                              advanced_payment = 'ADVANCED_PAYMENT',
                              retainer = 'RETAINER')


ProvisionRuleRole = Enum(author = 'author',
                         agent = 'agent')

ProvisionChannelType = Enum(book_and_ebook = '',
                            book = 'book',
                            ebook = 'ebook',
                            ebook_webshop = 'ebook::website',
                            ebook_external = 'ebook::indirect')


ProvisionChannelBase = Enum(net_price = 'NET_PRICE',
                            groos_price = 'GROSS_PRICE',
                            net_margin = 'NET_MARGIN',
                            gross_margin = 'GROSS_MARGIN')

UsersSearchType = Enum(email = 'email',
                       all_email = 'all_email',
                       user_id = 'user-id',
                       name = 'name')

Currency = Enum(AED = 'AED',
                AFN = 'AFN',
                ALL = 'ALL',
                AMD = 'AMD',
                ANG = 'ANG',
                AOA = 'AOA',
                ARS = 'ARS',
                AUD = 'AUD',
                AWG = 'AWG',
                AZN = 'AZN',
                BAM = 'BAM',
                BBD = 'BBD',
                BDT = 'BDT',
                BGN = 'BGN',
                BHD = 'BHD',
                BIF = 'BIF',
                BMD = 'BMD',
                BND = 'BND',
                BOB = 'BOB',
                BRL = 'BRL',
                BSD = 'BSD',
                BTN = 'BTN',
                BWP = 'BWP',
                BYR = 'BYR',
                BZD = 'BZD',
                CAD = 'CAD',
                CDF = 'CDF',
                CHF = 'CHF',
                CLP = 'CLP',
                CNY = 'CNY',
                COP = 'COP',
                CRC = 'CRC',
                CUP = 'CUP',
                CVE = 'CVE',
                CZK = 'CZK',
                DJF = 'DJF',
                DKK = 'DKK',
                DOP = 'DOP',
                DZD = 'DZD',
                EGP = 'EGP',
                ERN = 'ERN',
                ETB = 'ETB',
                EUR = 'EUR',
                FJD = 'FJD',
                FKP = 'FKP',
                GBP = 'GBP',
                GEL = 'GEL',
                GHS = 'GHS',
                GIP = 'GIP',
                GMD = 'GMD',
                GNF = 'GNF',
                GTQ = 'GTQ',
                GYD = 'GYD',
                HKD = 'HKD',
                HNL = 'HNL',
                HRK = 'HRK',
                HTG = 'HTG',
                HUF = 'HUF',
                IDR = 'IDR',
                ILS = 'ILS',
                INR = 'INR',
                IQD = 'IQD',
                IRR = 'IRR',
                ISK = 'ISK',
                JMD = 'JMD',
                JOD = 'JOD',
                JPY = 'JPY',
                KES = 'KES',
                KGS = 'KGS',
                KHR = 'KHR',
                KMF = 'KMF',
                KPW = 'KPW',
                KRW = 'KRW',
                KWD = 'KWD',
                KYD = 'KYD',
                KZT = 'KZT',
                LAK = 'LAK',
                LBP = 'LBP',
                LKR = 'LKR',
                LRD = 'LRD',
                LSL = 'LSL',
                LTL = 'LTL',
                LVL = 'LVL',
                LYD = 'LYD',
                MAD = 'MAD',
                MDL = 'MDL',
                MGA = 'MGA',
                MKD = 'MKD',
                MMK = 'MMK',
                MNT = 'MNT',
                MOP = 'MOP',
                MRO = 'MRO',
                MUR = 'MUR',
                MVR = 'MVR',
                MWK = 'MWK',
                MXN = 'MXN',
                MYR = 'MYR',
                MZN = 'MZN',
                NAD = 'NAD',
                NGN = 'NGN',
                NIO = 'NIO',
                NOK = 'NOK',
                NPR = 'NPR',
                NZD = 'NZD',
                OMR = 'OMR',
                PAB = 'PAB',
                PEN = 'PEN',
                PGK = 'PGK',
                PHP = 'PHP',
                PKR = 'PKR',
                PLN = 'PLN',
                PYG = 'PYG',
                QAR = 'QAR',
                RON = 'RON',
                RSD = 'RSD',
                RUB = 'RUB',
                RWF = 'RWF',
                SAR = 'SAR',
                SBD = 'SBD',
                SCR = 'SCR',
                SDG = 'SDG',
                SEK = 'SEK',
                SGD = 'SGD',
                SHP = 'SHP',
                SLL = 'SLL',
                SOS = 'SOS',
                SRD = 'SRD',
                STD = 'STD',
                SVC = 'SVC',
                SYP = 'SYP',
                SZL = 'SZL',
                THB = 'THB',
                TJS = 'TJS',
                TMT = 'TMT',
                TND = 'TND',
                TOP = 'TOP',
                TRY = 'TRY',
                TTD = 'TTD',
                TWD = 'TWD',
                TZS = 'TZS',
                UAH = 'UAH',
                UGX = 'UGX',
                USD = 'USD',
                UYU = 'UYU',
                UZS = 'UZS',
                VEF = 'VEF',
                VND = 'VND',
                VUV = 'VUV',
                WST = 'WST',
                XAF = 'XAF',
                XCD = 'XCD',
                XOF = 'XOF',
                XPF = 'XPF',
                YER = 'YER',
                ZAR = 'ZAR',
                ZMW = 'ZMW',
                ZWL = 'ZWL')

PreviewDisplayMode = Enum(auto = 'AUTO',
                          manual = 'MANUAL',
                          epub = 'EPUB',
                          xml = 'XML',
                          none = 'NONE')

PreviewTOCVisible = Enum(auto = 'AUTO',
                         yes = 'YES',
                         no = 'NO')


ProfileShow = Enum(no = 'NO',
                   yes = 'YES',
                   default = 'DEFAULT')

AssetsCoverType = Enum(distribution = 'distribution',
                       original = 'original',
                       big = 'big')

AssetsModules = Enum(cover = 'cover',
                     epub = 'epub',
                     mobi = 'mobi',
                     ibooks = 'ibooks',
                     audiobook = 'audiobook',
                     software = 'software',
                     pdf = 'pdf',
                     pod = 'pod',
                     extract = 'extract')

BookBinding = Enum(auto = 'AUTO',
                   pb = 'PB',
                   hc = 'HC',
                   bookelt = 'BOOKLET',
                   wireo = 'WIREO')

OrderItemType = Enum(document = 'DOCUMENT',
                     shipment = 'SHIPMENT',
                     fee = 'FEE',
                     tax = 'TAX')

ShippingStatus = Enum(new = 'new',
                      shipped = 'shipped',
                      delivered = 'delivered')

ShippingType = Enum(dhl = 'DHL',
                    fedex = 'FEDEX')

ShippingLevel = Enum(next_day = 'NextDay',
                     next_day_by_10_am = 'NextDayBy10am',
                     two_day = '2Day',
                     two_day_by_noon = '2DayByNoon',
                     three_day = '3Day',
                     three_to_five_day = '3To5Day',
                     three_to_seven_day = '3To7Day',
                     home_delivery = 'HomeDelivery')

ProcessingType = Enum(auto = 'AUTO',
                      yes = 'YES',
                      no = 'NO')

DRM = Enum(auto = 'AUTO',
           no = 'NO',
           watermark = 'WATERMARK',
           drm = 'DRM',
           adobe_drm = 'ADOBE_DRM')

