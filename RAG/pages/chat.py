import reflex as rx
from RAG.components.navbar import navbar
from RAG.states.rag_state import ChatState, MODEL_OPTIONS

def message_bubble(msg):
    is_user = (msg["role"] == "user")
    return rx.hstack(
        rx.cond(is_user, rx.spacer(), rx.fragment()),
        rx.box(
            rx.markdown(msg["content"]),
            bg=rx.cond(is_user, "#007bff", "#e5e5ea"),
            color=rx.cond(is_user, "white", "black"),
            padding="15px",
            border_radius="15px",
            max_width="70%",
        ),
        rx.cond(~is_user, rx.spacer(), rx.fragment()),
        width="100%",
        padding_y="2",
    )

def index():
    return rx.vstack(
        navbar(),
        
        # Chat area
        rx.box(
            rx.foreach(ChatState.history, message_bubble),
            height="75vh",
            overflow="auto",
            padding="20px",
            width="80%",
            bg="white",
            border="2px solid black",
            border_radius="10px",
            box_shadow="md",
            margin_top="20px"
        ),
        
        # Input area
        rx.form.root(
            rx.vstack(
               # Model Selector
rx.hstack(
    rx.text("Brain Power:", font_weight="bold", color="black"),

    rx.select(
        MODEL_OPTIONS,
        value=ChatState.selected_model_label,
        on_change=ChatState.set_selected_model_label,
        variant="classic",
        color_scheme="cyan",
        high_contrast=True,
        placeholder="Select Model",
        size="3",
        style={
            "backgroundColor": "white",
            "color": "black",
            "border": "2px solid black",
            "borderRadius": "10px",
            "padding": "10px 15px",
            "fontWeight": "bold",
            "width": "450px",
            "cursor": "pointer",
            "boxShadow": "0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)",
        },
        _hover={
            "box_shadow": "0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)",
            "border_color": "#ffffff",
            "background_color": "black",
        }
    ),

    width="80%",
    justify="start",
    align="center",
    margin_bottom="5px"
),
                
                # Chat Input and Send Button
                rx.hstack(
                    rx.input(
                        placeholder="Ask anything...",
                        value=ChatState.question,
                        on_change=ChatState.set_question,
                        width="80%",
                        size="3",
                        style={
                            "height": "100%",
                            "borderRadius": "10px",
                            "border": "2px solid black",
                            "backgroundColor": "white",
                            "--text-field-selection-color": "black",
                            "& input": {
                                "color": "black !important",
                                "fontWeight": "bold !important",
                                "WebkitTextFillColor": "black !important",
                            },
                            "& input::placeholder": {
                                "color": "#4b5563 !important",
                            }
                        }
                    ),
                    rx.button(
                        "Send",
                        type="submit",
                        bg="#007bff",
                        color="white",
                        padding="15px 30px",
                        border_radius="10px",
                        font_weight="bold",
                        _hover={"opacity": 0.8}
                    ),
                    width="80%",
                    padding_bottom="10px",
                ),
                width="100%",
                align_items="center",
            ),
            on_submit=ChatState.ask,
            width="100%",
            display="flex",
            justify_content="center",
        ),
        
        align_items="center",
        width="100%",
        height="100vh",
        background="#f5f5f5",
        spacing="0"
    )
