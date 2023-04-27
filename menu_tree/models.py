from django.db import models
from django.urls import reverse


class Menu(models.Model):
    title = models.CharField('Название', max_length=100)

    def __str__(self):
        return self.title


class MenuItem(models.Model):
    menu = models.ForeignKey('Menu', on_delete=models.CASCADE, related_name='items')
    title = models.CharField('Название', max_length=100)
    url = models.CharField('Ссылка', max_length=100, unique=True)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='child')

    class Meta:
        unique_together = ['menu', 'url']
        verbose_name = 'Menu item'
        verbose_name_plural = 'Menu items'

    def __str__(self):
        return self.title

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None, *args, **kwargs
    ):
        if not self.pk:
            self.url = reverse('detail', kwargs={'url': self.url})

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
        return parents

    def get_child(self, c=None):
        print(self)
        childs = MenuItem.objects.filter(parent=self)
        print(childs, 222)
        for item in childs:
            print(item, 23231)
            #if item['id'] in selected_item_id_list:
            #    item['child_items'] = get_child(items_values, item['id'], selected_item_id_list)
        if len(childs) > 0:
            return childs

        #child_url = [child.url for child in self.child.all()]
        return


    def set_relation(self):
        relations_of_parent = MenuRelation.objects.filter(from_parent=self.parent).values_list('to_child_id')
        relations = []
        for to_child_id in relations_of_parent:
            relations.append(MenuRelation(to_child_id=to_child_id[0], from_parent=self))
        relations.append(MenuRelation(to_child=self.parent, from_parent=self))
        MenuRelation.objects.bulk_create(relations)

    # TODO
    def delete(self, using=None, keep_parents=False):
        pass

    def get_absolute_url(self):
        return reverse(self.url)


class MenuRelation(models.Model):
    to_child = models.ForeignKey('MenuItem', on_delete=models.CASCADE, related_name='relations_with_parent')
    from_parent = models.ForeignKey('MenuItem', on_delete=models.CASCADE, related_name='relations_with_child')
