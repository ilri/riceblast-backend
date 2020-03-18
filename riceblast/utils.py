from riceapp.serializers.users import UserSerializer


def my_jwt_response_handler(access, user=None, request=None):
    return {
        'access': access,
        'user': UserSerializer(user, context={'request': request}).data,
    }