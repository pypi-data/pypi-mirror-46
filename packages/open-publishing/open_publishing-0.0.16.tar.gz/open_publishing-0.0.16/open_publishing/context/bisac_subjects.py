from open_publishing.core.enums import BisacCode, VLBCategory
from open_publishing.bisac import BisacSubject

class BisacSubjects(object):
    def __init__(self,
                 context):
        self._ctx = context

    def load(self,
             bisac_code=None,
             internal_id=None):
        if len([i for i in [bisac_code, internal_id] if i is not None]) != 1:
            raise ValueError('Only one of bisac_code/internal_id should be specified')
        elif bisac_code is not None:
            if bisac_code in BisacCode:
                subject_id = self._ctx.gjp.resolve_enum(BisacCode,
                                                        enum=bisac_code).internal_id
            else:
                subject_id = self._ctx.gjp.resolve_enum(BisacCode,
                                                        code=bisac_code).internal_id
        elif internal_id is not None:
            subject_id = internal_id
        return BisacSubject(self._ctx,
                            subject_id)

        

    def search(self,
               vlb_category):
        if vlb_category is None:
            raise ValueError("vlb_category should not be None")
        elif vlb_category in VLBCategory:
            category_id = self._ctx.gjp.resolve_enum(VLBCategory,
                                                     enum=vlb_category).internal_id
        else:
            category_id = self._ctx.gjp.resolve_enum(VLBCategory,
                                                     code=vlb_category).internal_id
            
        subject_ids = self._ctx.gjp.vlb_to_bisac(category_id)

        subjects = []
        for subject_id in subject_ids:
            subjects.append(BisacSubject(self._ctx,
                                    subject_id))
        return subjects

        
    
