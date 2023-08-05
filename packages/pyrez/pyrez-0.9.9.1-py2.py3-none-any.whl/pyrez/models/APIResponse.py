from .APIResponseBase import APIResponseBase
class APIResponse(APIResponseBase):
    def __init__(self, **kwargs):
    	super().__init__(**kwargs)
    	self.errorMsg = kwargs.get("ret_msg", kwargs.get("error", kwargs.get("errors", None))) if kwargs else None
    def hasError(self):
        return self.errorMsg is not None
