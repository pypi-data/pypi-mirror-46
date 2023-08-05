from swiss_common_utils.services.swiss_service_base import SWISSServiceBase


class ModelBuilderService(SWISSServiceBase):

    def get_model(self):
        path_params_list = ['getmodel/']
        url = self._get_url(path_params_list=path_params_list)
        response = super().dispatch(url=url)
        return super()._handle_response(response)
