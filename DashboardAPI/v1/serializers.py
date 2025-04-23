from rest_framework import serializers
from users.models import CustomUser, Farm, FarmMembership, FarmGroup, ExternalOrganization, ExternalOrganizationMembership


class UserFarmsSerializer(serializers.ModelSerializer):
    """Сериализатор для отображения информации о ферме пользователя.

    Включает базовую информацию о ферме и полное имя владельца.
    """
    owner_full_name = serializers.SerializerMethodField()
    organization_name = serializers.SerializerMethodField()


    class Meta:
        model = Farm
        fields = ['id', 'name', 'description', 'owner_full_name', 'organization_name']
        """
        Поля:
            id (int): Уникальный идентификатор фермы
            name (str): Название фермы
            description (str): Описание фермы
            owner_full_name (str): Полное имя владельца фермы (first_name + last_name)
        """

    @staticmethod
    def get_owner_full_name(obj):
        """Генерирует полное имя владельца фермы.

        Args:
            obj (Farm): Объект фермы

        Returns:
            str: Строка в формате "{first_name} {last_name}"
        """
        return f"{obj.owner.first_name} {obj.owner.last_name}"

    @staticmethod
    def get_organization_name(obj):
        """Возвращает название организации - владельца фермы.

        Args:
            obj (Farm): Объект фермы

        Returns:
            str: Строка"
        """
        return f"{obj.organization.name}"


class UserFarmMembershipsSerializer(serializers.ModelSerializer):
    """Сериализатор для членства пользователя в ферме.

    Включает:
    - полную информацию о ферме через UserFarmsSerializer
    - даты в формате "дд.мм.гггг чч:мм"
    - все поля модели FarmMembership
    """
    farm = UserFarmsSerializer()
    joined_at = serializers.DateTimeField(format="%d.%m.%Y %H:%M")
    updated_at = serializers.DateTimeField(format="%d.%m.%Y %H:%M")

    class Meta:
        model = FarmMembership
        fields = '__all__'
        """
        Поля модели FarmMembership:
            id (int): Уникальный идентификатор членства
            user (int): ID пользователя (ForeignKey)
            farm (dict): Информация о ферме (сериализованная через UserFarmsSerializer)
            role (str): Роль пользователя в ферме (owner/admin/manager/technician/viewer)
            joined_at (str): Дата присоединения в формате "дд.мм.гггг чч:мм"
            updated_at (str): Дата обновления в формате "дд.мм.гггг чч:мм"
        """


class UserExternalOrganizationSerializer(serializers.ModelSerializer):
    """Сериализатор для краткого представления внешней организации.

    Используется для вложенного отображения организации в других сериализаторах.
    Выводит только базовые поля, исключая敏感ные или избыточные данные.

    Attributes:
        id (int): Уникальный идентификатор организации.
        name (str): Название организации.
        address (str): Физический адрес организации (опционально).
        description (str): Описание деятельности организации (опционально).
    """

    class Meta:
        model = ExternalOrganization
        fields = ['id', 'name', 'address', 'description']


class UserExternalOrganizationMembershipsSerializer(serializers.ModelSerializer):
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
    organization = UserExternalOrganizationSerializer()
    updated_at = serializers.DateTimeField(format="%d.%m.%Y %H:%M")

    class Meta:
        model = ExternalOrganizationMembership
        fields = ['id', 'organization', 'role', 'status', 'updated_at']