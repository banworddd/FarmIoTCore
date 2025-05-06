from rest_framework import serializers
from users.models import CustomUser,  ExternalOrganizationMembership, ExternalOrganization


class ExternalOrganizationSerializer(serializers.ModelSerializer):

    class Meta:
        model = ExternalOrganization
        fields = ['name', 'type', 'address', 'email', 'phone', 'website', 'description', 'created_at', 'updated_at']


class ExternalOrganizationUserSerializer(serializers.ModelSerializer):

    user_full_name = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ['user_full_name', 'phone_number', 'email']

    @staticmethod
    def get_user_full_name(obj):
        """Генерирует полное имя владельца фермы.


        Returns:
            str: Строка в формате "{first_name} {last_name}"
        """
        return f"{obj.first_name} {obj.last_name}"


class ExternalOrganizationUsersSerializer(serializers.ModelSerializer):
    """Сериализатор для членства пользователя в организации.

    Детализирует связь пользователя с организацией, включая:
    - полные данные организации через вложенный сериализатор
    - роль пользователя
    - статус подтверждения членства
    - дату последнего обновления в удобном формате

    Attributes:
        id (int): Уникальный идентификатор записи о членстве.
        organization (dict): Сериализованные данные организации (UserExternalOrganizationSerializer).
        role (str): Роль пользователя в организации (например, 'admin', 'member').
        status (str): Статус членства ('approved', 'pending', 'rejected').
        updated_at (str): Дата последнего обновления в формате 'DD.MM.YYYY HH:MM'.
    """
    updated_at = serializers.DateTimeField(format="%d.%m.%Y %H:%M")
    user =  ExternalOrganizationUserSerializer()

    class Meta:
        model = ExternalOrganizationMembership
        fields = ['id', 'user', 'role', 'status', 'updated_at']
        read_only_fields = ['id', 'user', 'updated_at']








