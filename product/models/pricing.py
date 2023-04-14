from django.db import models


class ProductPricing(models.Model):
    product = models.ForeignKey("product.Product", on_delete=models.CASCADE)
    petshop = models.ForeignKey("product.Petshop", on_delete=models.CASCADE)
    price = models.PositiveIntegerField()
    price_after_sale = models.PositiveIntegerField(null=True, blank=True)
    inventory = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True,null=True)

    class Meta:
        unique_together = ("product_id", "petshop_id")

    @property
    def is_on_sale(self):
        return (
            self.price_after_sale is not None
            and self.price_after_sale < self.price
        )

    @property
    def discount(self):
        if self.is_on_sale:
            return ((self.price - self.price_after_sale) / self.price) * 100
        else:
            return 0
