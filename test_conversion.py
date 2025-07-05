import logging
from tools.md_to_docx.md_to_docx import MarkdownToDocxTool

# 配置日志
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def test_conversion():
    try:
        # 读取测试文档
        logger.info("读取测试文档...")
        with open("test_document.md", "r", encoding="utf-8") as f:
            md_content = f.read()
        
        logger.info("创建转换工具实例...")
        # 创建转换工具实例
        converter = MarkdownToDocxTool()
        
        # 准备参数
        params = {
            "md_text": md_content,
            "output_filename": "test_output.docx"
        }
        
        logger.info("开始转换...")
        # 执行转换
        for message in converter._invoke(params):
            if hasattr(message, "blob"):
                # 保存输出文件
                logger.info("保存输出文件...")
                with open("test_output.docx", "wb") as f:
                    f.write(message.blob)
                logger.info("转换完成，请查看 test_output.docx")
            else:
                logger.info(f"消息: {message.text}")
    except Exception as e:
        logger.exception("转换过程中出现错误:")

if __name__ == "__main__":
    test_conversion()
