from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType

from app.core.config import settings
from app.database import Order


class EmailService:

    def __init__(self):
        self.conf = ConnectionConfig(
            MAIL_USERNAME="",
            MAIL_PASSWORD="",
            MAIL_SERVER=settings.mail_server,
            MAIL_PORT=settings.mail_port,
            MAIL_FROM=settings.mail_from,
            MAIL_STARTTLS=settings.mail_starttls,
            MAIL_SSL_TLS=settings.mail_ssl_tls,
            USE_CREDENTIALS=settings.use_credentials,
            VALIDATE_CERTS=False,
        )
        self.fm = FastMail(self.conf)


    def _build_order_confirmation_html(self, order: Order) -> str:
        items_rows = "".join(
            f"""
            <tr>
                <td style="padding: 12px 8px; border-bottom: 1px solid #e5e5e5;">{item.variant.name}</td>
                <td style="padding: 12px 8px; border-bottom: 1px solid #e5e5e5; text-align: center;">{item.quantity}</td>
                <td style="padding: 12px 8px; border-bottom: 1px solid #e5e5e5; text-align: right;">{item.price} ₽</td>
                <td style="padding: 12px 8px; border-bottom: 1px solid #e5e5e5; text-align: right;">{item.price * item.quantity} ₽</td>
            </tr>
            """
            for item in order.items
        )

        return f"""
        <html>
        <body style="font-family: Arial, sans-serif; background-color: #f4f4f4; padding: 24px; margin: 0;">
            <div style="max-width: 600px; margin: 0 auto; background: #ffffff; border-radius: 8px; overflow: hidden;">

                <div style="background-color: #1a1a1a; padding: 24px; text-align: center;">
                    <h1 style="color: #ffffff; margin: 0; font-size: 20px;">Спасибо за заказ!</h1>
                </div>

                <div style="padding: 24px;">
                    <p style="color: #333; font-size: 15px;">
                        Ваш заказ <strong>#{order.id}</strong> успешно оплачен и передан в обработку.
                    </p>

                    <table style="width: 100%; border-collapse: collapse; margin-top: 16px;">
                        <thead>
                            <tr style="background-color: #fafafa;">
                                <th style="padding: 10px 8px; text-align: left; font-size: 13px; color: #888;">Товар</th>
                                <th style="padding: 10px 8px; text-align: center; font-size: 13px; color: #888;">Кол-во</th>
                                <th style="padding: 10px 8px; text-align: right; font-size: 13px; color: #888;">Цена</th>
                                <th style="padding: 10px 8px; text-align: right; font-size: 13px; color: #888;">Сумма</th>
                            </tr>
                        </thead>
                        <tbody>
                            {items_rows}
                        </tbody>
                    </table>

                    <div style="margin-top: 16px; text-align: right; font-size: 15px; color: #333;">
                        <p style="margin: 4px 0;">Скидка: <strong>-{order.discount_amount} ₽</strong></p>
                        <p style="margin: 4px 0; font-size: 18px;">Итого: <strong>{order.total_amount} ₽</strong></p>
                    </div>
                </div>

                <div style="background-color: #fafafa; padding: 16px 24px; text-align: center;">
                    <p style="color: #999; font-size: 12px; margin: 0;">
                        Это письмо сгенерировано автоматически, отвечать на него не нужно.
                    </p>
                </div>

            </div>
        </body>
        </html>
        """


    async def send_order_confirmation(
            self, order: Order, user_email: str,
    ) -> None:
        html = self._build_order_confirmation_html(order=order)
        message = MessageSchema(
            subject=f"Заказ #{order.id} оплачен",
            recipients=[user_email],
            body=html,
            subtype=MessageType.html,
        )
        await self.fm.send_message(message=message)