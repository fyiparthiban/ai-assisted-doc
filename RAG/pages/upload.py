import reflex as rx
from RAG.components.navbar import navbar
from RAG.components.footer import footer
from RAG.states.rag_state import ChatState

def index():
    return rx.vstack(
        navbar(),
        rx.center(
            rx.vstack(
                rx.heading("Upload Documents", margin_bottom="20px", color="black", font_weight="bold"),
                rx.text("Upload your PDF, DOCX, PPTX, and TXT files for the RAG AI to read.", margin_bottom="20px", color="black", font_weight="bold"),
                rx.upload(
                    rx.vstack(
                        rx.button("Select Files", bg="black", color="white", border_radius="10px", size="3"),
                        rx.text("📂 Drag and drop files here or click to select files", color="black", font_weight="bold"),
                        align="center",
                        spacing="2",
                    ),
                    id="doc_upload",
                    multiple=True,
                    padding="4em",
                    border="2px dashed #007bff",
                    border_radius="15px",
                    bg="#f0f7ff",
                    on_drop=ChatState.handle_upload(rx.upload_files(upload_id="doc_upload")),
                    _hover={
                        "border": "2px dashed #0056b3",
                        "bg": "#e6f2ff",
                        "transition": "0.3s ease-in-out",
                    }
                ),
                
                # Success Dialog
                rx.alert_dialog.root(
                    rx.alert_dialog.content(
                        rx.alert_dialog.title("✅ Upload Successful!", color="black", font_weight="bold"),
                        rx.alert_dialog.description(
                            "Your documents have been processed and indexed. What would you like to do next?",
                            color="#333",
                        ),
                        rx.hstack(
                            rx.alert_dialog.cancel(
                                rx.button(
                                    "📎 Upload More", 
                                    on_click=ChatState.toggle_upload_dialog,
                                    variant="outline",
                                    color="black",
                                    border="1px solid #ccc",
                                    _hover={"bg": "#f5f5f5"}
                                ),
                            ),
                            rx.alert_dialog.action(
                                rx.button(
                                    "🚀 Let's Chat", 
                                    on_click=rx.redirect("/chat"),
                                    bg="#007bff",
                                    color="white",
                                    _hover={"opacity": 0.8}
                                ),
                            ),
                            margin_top="20px",
                            justify="end",
                            spacing="3",
                        ),
                        border_radius="15px",
                        padding="30px",
                        bg="white",
                        box_shadow="xl",
                        style={"max_width": "450px"}
                    ),
                    open=ChatState.show_upload_dialog,
                ),
                rx.text("Uploaded Files:", font_weight="bold", margin_top="20px", color="black"),
                rx.foreach(ChatState.uploaded_files, lambda file: rx.text(file, color="black", font_weight="bold")),
                width="50%",
                padding="20px",
                box_shadow="lg",
                border_radius="lg",
                bg="white"
            ),
            width="100%",
            height="80vh",
        ),
        footer(),
        min_height="100vh",
        spacing="0",
        background="#f5f5f5"
    )
