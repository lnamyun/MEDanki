from unstructured.partition.pdf import partition_pdf
import os

from pdf2image import convert_from_path

images = convert_from_path(
    pdf_path,
    poppler_path="/usr/bin"  # 또는 "/usr/local/bin"으로 바꿔서 시도 가능
)

def extract_text_and_images_from_pdf(pdf_path, output_dir="extracted"):
    elements = partition_pdf(
        filename=pdf_path,
        extract_images_in_pdf=True,
        output_image_dir_path=output_dir
    )

    # 텍스트와 이미지 정보 분리
    texts = [el.text for el in elements if el.text]
    images = [el.metadata.image_path for el in elements if hasattr(el.metadata, 'image_path') and el.metadata.image_path]

    return texts, images
