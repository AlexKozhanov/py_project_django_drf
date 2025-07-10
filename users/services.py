import stripe
from config.settings import STRIPE_API_KEY
from Ims.models import Course

stripe.api_key = STRIPE_API_KEY


def create_stripe_product(course: Course) -> str:
    """Создает продукт в Stripe и возвращает его ID."""
    product_data = {
        "name": course.name,
    }

    # Добавляем описание, только если оно есть
    if course.description:
        product_data["description"] = course.description

    product = stripe.Product.create(**product_data)
    return product.id


def create_stripe_price(product_id: str, amount: int) -> str:
    """Создает цену в Stripe и возвращает ее ID."""
    price = stripe.Price.create(
        currency="rub",
        product=product_id,
        unit_amount=amount * 100,  # Переводим в копейки
    )
    return price.id


def create_stripe_session(price_id: str, success_url: str, cancel_url: str) -> dict:
    """Создает сессию оплаты в Stripe и возвращает данные сессии."""
    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[{"price": price_id, "quantity": 1, }],
        mode="payment",
        success_url=success_url,
        # cancel_url=cancel_url,
    )
    return {"session_id": session.id, "payment_link": session.url}
