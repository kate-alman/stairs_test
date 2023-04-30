from django.db import models
from django.urls import reverse


class Menu(models.Model):
    title = models.CharField("Название", max_length=100)

    def __str__(self):
        return self.title


class MenuItem(models.Model):
    menu = models.ForeignKey("Menu", on_delete=models.CASCADE, related_name="items")
    title = models.CharField("Название", max_length=100)
    url = models.CharField("Ссылка", max_length=100, unique=True)
    parent = models.ForeignKey(
        "self", on_delete=models.SET_NULL, null=True, blank=True, related_name="child"
    )

    class Meta:
        unique_together = ["menu", "url"]
        verbose_name = "Menu item"
        verbose_name_plural = "Menu items"

    def __str__(self):
        return self.title

    def save(
        self,
        force_insert=False,
        force_update=False,
        using=None,
        update_fields=None,
        *args,
        **kwargs,
    ) -> None:
        if not self.pk:
            self.url = reverse("detail", kwargs={"url": self.url})

            super().save(*args, **kwargs)
            if self.parent:
                self.set_relation()
            return

    def get_parents(self, last=None, parents=None) -> list[str]:
        parents = [] if not parents else parents
        if not last:
            last = self
        parents.append(last)
        if last.parent:
            self.get_parents(last.parent, parents)
        return parents[1:]

    def set_relation(self) -> None:
        relations_of_parent = MenuRelation.objects.filter(
            from_parent=self.parent
        ).values_list("to_child_id")
        relations = []
        for to_child_id in relations_of_parent:
            relations.append(MenuRelation(to_child_id=to_child_id[0], from_parent=self))
        relations.append(MenuRelation(to_child=self.parent, from_parent=self))
        MenuRelation.objects.bulk_create(relations)

    def get_absolute_url(self):
        return reverse(self.url)


class MenuRelation(models.Model):
    to_child = models.ForeignKey(
        "MenuItem", on_delete=models.CASCADE, related_name="relations_with_parent"
    )
    from_parent = models.ForeignKey(
        "MenuItem", on_delete=models.CASCADE, related_name="relations_with_child"
    )

    class Meta:
        verbose_name = "MenuRelation"
        verbose_name_plural = "MenuRelations"

    def __str__(self):
        return f"From {self.from_parent} to {self.to_child}"
