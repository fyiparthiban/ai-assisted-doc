import reflex as rx

config = rx.Config(
    app_name="practice_ui",
    # api_url="https://698eef83-51f3-4304-b63b-20f1a57cb81e.fly.dev/",
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
    ]
)
