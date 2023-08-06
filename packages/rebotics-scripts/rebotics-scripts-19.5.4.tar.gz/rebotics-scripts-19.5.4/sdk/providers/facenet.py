from six import StringIO, wraps

from .base import ReboticsBaseProvider, remote_service


def required_model_params(params=None):
    if params is None:
        params = ['model_path', 'index_path', 'meta_path']

    def outer(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            model_params = {
                key: kwargs[key] for key in params
            }
            kwargs['model_params'] = {
                'model_path': model_params['model_path'],
                'model_index_path': model_params['index_path'],
                'model_meta_path': model_params['meta_path']
            }
            result = func(*args, **kwargs)
            return result
        return wrapper

    if callable(params):
        return outer(params)

    return outer


class FacenetProvider(ReboticsBaseProvider):
    timeout = 180
    retries = 2

    @required_model_params()
    @remote_service('/images_feature_vectors/')
    def extract_from_image(self, images_io, model_params, **kwargs):
        """Extraction of the feature vectors from image IO"""
        # Expects to have .npy (numpy array) load from cv2.load
        return self.session.post(data=model_params, files=[
            ('images', ('image%d.png' % i, StringIO(image), 'image/png'))
            for i, image in enumerate(images_io)
        ])

    @required_model_params()
    @remote_service('/image_url_feature_vector/')
    def extract_from_image_url(self, images_url, model_params, **kwargs):
        data = model_params
        data['image_link'] = images_url
        return self.session.post(data=data)

    @required_model_params()
    @remote_service('/keyframe_feature_vectors/')
    def extract_from_keyframe(self, keyframe_url, bboxes, model_params, **kwargs):
        data = model_params
        data['bboxes'] = bboxes
        data['keyframe_url'] = keyframe_url
        return self.session.post(data=data)

    @required_model_params()
    @remote_service('/keyframe_image_feature_vector/')
    def extract_from_keyframe_image(self, keyframe_io, bboxes, use_fixed_image_standardization, model_params, **kwargs):
        # Expects to have .npy (numpy array) load from cv2.load
        data = model_params
        data['bboxes'] = bboxes
        data['use_fixed_image_standardization'] = use_fixed_image_standardization
        return self.session.post(
            data=data, files={
                'images': StringIO(keyframe_io)
            }
        )
