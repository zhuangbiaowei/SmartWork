from typing import Dict, Any
from .llm_client import LLMClient


class ContentGenerator:
    """
    AI-powered content generator using LLM.

    Generates various types of content including reports, summaries,
    and other documents based on provided data and topics.
    """

    def __init__(self, llm_client: LLMClient):
        self.llm_client = llm_client

    async def generate_report(self, topic: str, data: Dict[str, Any]) -> str:
        """
        Generate a professional report based on data.

        Args:
            topic: Report topic/title
            data: Dictionary with data to include in report

        Returns:
            Generated report content
        """
        prompt = f"""
请基于以下数据生成一份专业的报告：

主题: {topic}

数据: {data}

报告应该包含:
1. 执行摘要
2. 详细分析
3. 结论和建议

请使用专业、清晰的语言格式化报告。
        """

        return await self.llm_client.generate(prompt)

    async def generate_summary(self, content: str) -> str:
        """
        Generate a concise summary of content.

        Args:
            content: Content to summarize

        Returns:
            Generated summary
        """
        prompt = f"""
请将以下内容总结为简洁的摘要（不超过 200 字）:

{content}

摘要应该包含主要观点和关键结论。
        """

        return await self.llm_client.generate(prompt, max_tokens=300)

    async def generate_email(
        self, recipient: str, subject: str, content_points: list
    ) -> str:
        """
        Generate a professional email.

        Args:
            recipient: Email recipient name
            subject: Email subject
            content_points: List of key points to include

        Returns:
            Generated email content
        """
        points_str = "\n".join([f"- {point}" for point in content_points])

        prompt = f"""
请生成一封给 {recipient} 的专业邮件：

主题: {subject}

要点:
{points_str}

邮件应该:
1. 使用正式但友好的语气
2. 逻辑清晰地组织内容
3. 包含适当的问候和结尾
        """

        return await self.llm_client.generate(prompt)

    async def generate_meeting_agenda(
        self, meeting_purpose: str, attendees: list, duration_minutes: int
    ) -> str:
        """
        Generate a meeting agenda.

        Args:
            meeting_purpose: Purpose of the meeting
            attendees: List of attendee names
            duration_minutes: Expected meeting duration

        Returns:
            Generated meeting agenda
        """
        attendees_str = ", ".join(attendees)

        prompt = f"""
请生成一个会议议程：

会议目的: {meeting_purpose}
参会人员: {attendees_str}
预计时长: {duration_minutes} 分钟

议程应该:
1. 按时间顺序组织
2. 为每个议程项分配时间
3. 包含预期的讨论结果
        """

        return await self.llm_client.generate(prompt)
