import utils
from elg import FlaskService
from elg.model import Failure
from elg.model import ClassificationResponse
from elg.model import TextRequest, StructuredTextRequest
from elg.model import ClassesResponse
from elg.model.base import StandardMessages


class SwedishSentCLF(FlaskService):
    def process_single_text(self, text):
        """Single text handler that catches too large request and
        internal exception while parsing text"""
        if utils.is_exceed_limit(text):
            tooLargeMessage = StandardMessages.\
                    generate_elg_request_too_large()
            return Failure(errors=[tooLargeMessage])
        try:
            res = utils.clf_func_elg(text)
        except Exception as err:
            internalErrorMessage = StandardMessages.\
                    generate_elg_service_internalerror(
                        params=[str(err)])
            return Failure(errors=[internalErrorMessage])
        return res

    def process_text(self, request: TextRequest):
        text = request.content
        res = self.process_single_text(text)
        if isinstance(res, ClassesResponse):
            return ClassificationResponse(classes=[res])
        else:  # failure
            return res


flask_service = SwedishSentCLF("sent-sv")
app = flask_service.app
