import pytest
from app.models.ai_processor import AIProcessor

def test_summarize_success():
    """
    Probar el resumen exitoso de un contenido válido.
    """
    ai_processor = AIProcessor(api_key="test_key", model_name="test_model")
    summary = ai_processor.summarize("Este es un texto de prueba.")
    assert summary == "Resumen generado."

def test_translate_success():
    """
    Probar la traducción exitosa de un contenido válido.
    """
    ai_processor = AIProcessor(api_key="test_key", model_name="test_model")
    translation = ai_processor.translate("Hola", "en")
    assert translation == "Contenido traducido."

def test_modify_content_success():
    """
    Probar la modificación exitosa de un contenido con instrucciones.
    """
    ai_processor = AIProcessor(api_key="test_key", model_name="test_model")
    modified_content = ai_processor.modify_content("Texto inicial", "Hazlo más formal.")
    assert modified_content == "Contenido modificado."

def test_summarize_invalid_content():
    """
    Probar que resumir contenido inválido (vacío) lanza un ValueError.
    """
    ai_processor = AIProcessor(api_key="test_key", model_name="test_model")
    with pytest.raises(ValueError):
        ai_processor.summarize("")

def test_translate_missing_language():
    """
    Probar que traducir sin especificar un idioma destino lanza un ValueError.
    """
    ai_processor = AIProcessor(api_key="test_key", model_name="test_model")
    with pytest.raises(ValueError):
        ai_processor.translate("Hola", "")

def test_translate_invalid_content():
    """
    Probar que traducir contenido inválido (vacío) lanza un ValueError.
    """
    ai_processor = AIProcessor(api_key="test_key", model_name="test_model")
    with pytest.raises(ValueError):
        ai_processor.translate("", "en")

def test_modify_content_missing_instructions():
    """
    Probar que modificar contenido sin instrucciones lanza un ValueError.
    """
    ai_processor = AIProcessor(api_key="test_key", model_name="test_model")
    with pytest.raises(ValueError):
        ai_processor.modify_content("Texto inicial", "")

def test_modify_content_invalid_content():
    """
    Probar que modificar contenido inválido (vacío) lanza un ValueError.
    """
    ai_processor = AIProcessor(api_key="test_key", model_name="test_model")
    with pytest.raises(ValueError):
        ai_processor.modify_content("", "Hazlo más formal.")
