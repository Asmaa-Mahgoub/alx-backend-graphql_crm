import graphene
from crm.models import Product

class ProductType(graphene.ObjectType):
    id = graphene.ID()
    name = graphene.String()
    stock = graphene.Int()

class UpdateLowStockProducts(graphene.Mutation):
    class Arguments:
        increment_by = graphene.Int(default_value=10)

    updated_products = graphene.List(ProductType)
    success = graphene.Boolean()
    message = graphene.String()

    def mutate(self, info, increment_by):
        # Get products with stock < 10
        low_stock_products = Product.objects.filter(stock__lt=10)
        updated_products_list = []

        for product in low_stock_products:
            product.stock += increment_by
            product.save()
            updated_products_list.append(product)

        return UpdateLowStockProducts(
            updated_products=updated_products_list,
            success=True,
            message=f"Updated {len(updated_products_list)} low-stock products"
        )

class Mutation(graphene.ObjectType):
    updateLowStockProducts = UpdateLowStockProducts.Field()

schema = graphene.Schema(mutation=Mutation)
