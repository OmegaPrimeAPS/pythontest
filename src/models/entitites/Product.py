class Product:
    def init(self, id, sku=None, name=None, price=None, brand=None) -> None:
        self.id = id
        self.sku = sku
        self.name = name
        self.price = price
        self.brand = brand

    def to_JSON(self):
        return {
            "id": self.id,
            "sku": self.sku,
            "name": self.name,
            "price": str(
                self.price
            ),  # convert float value into string for JSON serialization
            "brand": self.brand,
        }
