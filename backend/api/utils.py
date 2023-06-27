

class RepeatableMixin:
    """Миксин для повторяющегося кода."""

    def check_if_already_added(self, model, user, recipe):
        """Проверка на то, добавлен ли уже рецепт."""
        if model.objects.filter(user=user, recipe=recipe).exists():
            return True
        return False

    def create_and_serialize(self, serializer_class, model, user, recipe):
        """Создание экземпляра и сериализация."""
        instance = model.objects.create(user=user, recipe=recipe)
        serializer = serializer_class(instance.recipe)
        return serializer.data

    def delete_instance(self, model, user, recipe_id):
        """Удаление экземпляра."""
        instance = model.objects.filter(user=user, recipe=recipe_id)
        if instance.exists():
            instance.delete()
            return True
        return False
