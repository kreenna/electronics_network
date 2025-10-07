from django.core.exceptions import ValidationError
from django.db import models


class ContactInfo(models.Model):  # контакты звена сети
    email = models.EmailField()
    country = models.CharField(max_length=100, verbose_name="Страна")
    city = models.CharField(max_length=100, verbose_name="Город")
    street = models.CharField(max_length=100, verbose_name="Улица")
    house_number = models.CharField(max_length=20, verbose_name="Дом")

    class Meta:
        abstract = True


class Product(models.Model):  # сам продукт
    name = models.CharField(max_length=255, verbose_name="Название")
    model = models.CharField(max_length=255, verbose_name="Модель")
    release_date = models.DateField(verbose_name="Дата выхода на рынок")

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"

    def __str__(self):
        return f"{self.name} ({self.model})"


class Factory(ContactInfo):  # завод
    name = models.CharField(max_length=255, verbose_name="Название")

    # поставщиком может быть только другой завод
    supplier = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True,
                                 related_name="factories_supplied", verbose_name="Поставщик (завод)")

    debt_to_supplier = models.DecimalField(max_digits=12, decimal_places=2, default=0,
                                           verbose_name="Задолженность поставщику")
    created_at = models.DateTimeField(auto_now_add=True)
    products = models.ManyToManyField(Product, blank=True, verbose_name="Продукты")

    class Meta:
        verbose_name = "Завод"
        verbose_name_plural = "Заводы"

    def clean(self):
        # проверяем, что поставщик у завода только завод (сам или другой)
        if self.supplier and not isinstance(self.supplier, Factory):
            raise ValidationError("Поставщик завода должен быть заводом.")

    def __str__(self):
        return f"Завод: {self.name}"


class RetailNetwork(ContactInfo):  # розничная сеть
    name = models.CharField(max_length=255, verbose_name="Название")

    # поставщик либо завод, либо другая сеть
    supplier_factory = models.ForeignKey(Factory, on_delete=models.PROTECT, null=True, blank=True,
                                         related_name="retail_networks_supplied", verbose_name="Поставщик (завод)")
    supplier_network = models.ForeignKey("self", on_delete=models.PROTECT, null=True, blank=True,
                                         related_name="networks_supplied", verbose_name="Поставщик (сеть)")

    debt_to_supplier = models.DecimalField(max_digits=12, decimal_places=2, default=0,
                                           verbose_name="Задолженность поставщику")
    created_at = models.DateTimeField(auto_now_add=True)
    products = models.ManyToManyField(Product, blank=True, verbose_name="Продукты")

    class Meta:
        verbose_name = "Розничная сеть"
        verbose_name_plural = "Розничные сети"

    def clean(self):
        # проверяем, что поставщик ровно один: либо завод, либо другая сеть
        if bool(self.supplier_factory) == bool(self.supplier_network):
            raise ValidationError("Розничная сеть должна иметь ровно одного поставщика: завод или сеть.")

    def __str__(self):
        return f"Розничная сеть: {self.name}"


class IndividualEntrepreneur(ContactInfo):  # ИП
    name = models.CharField(max_length=255, verbose_name="Название")

    # поставщик либо завод, розничная сеть или же другой ИП
    supplier_factory = models.ForeignKey(Factory, on_delete=models.PROTECT, null=True, blank=True,
                                         related_name="ie_supplied_by_factory", verbose_name="Поставщик (завод)")
    supplier_retail = models.ForeignKey(RetailNetwork, on_delete=models.PROTECT, null=True, blank=True,
                                        related_name="ie_supplied_by_retail", verbose_name="Поставщик (сеть)")
    supplier_ie = models.ForeignKey("self", on_delete=models.PROTECT, null=True, blank=True,
                                    related_name="ie_supplied_by_ie", verbose_name="Поставщик (ИП)")

    debt_to_supplier = models.DecimalField(max_digits=12, decimal_places=2, default=0,
                                           verbose_name="Задолженность поставщику")
    created_at = models.DateTimeField(auto_now_add=True)
    products = models.ManyToManyField(Product, blank=True, verbose_name="Продукты")

    class Meta:
        verbose_name = "Индивидуальный предприниматель"
        verbose_name_plural = "Индивидуальные предприниматели"

    def clean(self):
        # проверяем, что поставщик выбран только один: завод, розничная сеть или другой ИП
        suppliers = [bool(self.supplier_factory), bool(self.supplier_retail), bool(self.supplier_ie)]
        if suppliers.count(True) != 1:
            raise ValidationError("ИП должен иметь ровно одного поставщика: завод, розничная сеть или ИП.")

    def __str__(self):
        return f"Индивидуальный предприниматель: {self.name}"
