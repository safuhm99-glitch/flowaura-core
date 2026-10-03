import type { NextApiRequest, NextApiResponse } from 'next';
import OpenAI from 'openai';

const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
});

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method !== 'POST') {
    return res.status(405).json({ success: false, message: 'الطريقة غير مسموحة، استخدم POST فقط' });
  }

  try {
    const { userPrompt } = req.body;

    if (!userPrompt) {
      return res.status(400).json({ success: false, message: 'الرجاء إدخال وصف النص' });
    }

    const completion = await openai.chat.completions.create({
      model: "gpt-4o",
      messages: [
        { 
          role: "system", 
          content: "You are an expert AI prompt engineer. Translate the user prompt to English if it's in Arabic, and optimize it into a highly detailed, professional 3D asset generation prompt for Meshy AI. Respond ONLY with the optimized English prompt text, no explanations." 
        },
        { role: "user", content: userPrompt }
      ],
    });

    const optimizedPrompt = completion.choices[0]?.message?.content?.trim();

    if (!optimizedPrompt) {
      throw new Error('فشل OpenAI في تحسين الوصف.');
    }

    const meshyResponse = await fetch('https://api.meshy.ai/v2/text-to-3d', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${process.env.MESHY_API_KEY}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        mode: 'preview',
        prompt: optimizedPrompt,
        art_style: 'realistic',
      }),
    });

    const meshyData = await meshyResponse.json();

    if (!meshyResponse.ok || !meshyData.result) {
      throw new Error(meshyData.message || 'حدث خطأ أثناء إرسال الطلب لـ Meshy AI');
    }

    return res.status(200).json({ 
      success: true, 
      taskId: meshyData.result, 
      optimizedPrompt: optimizedPrompt,
      message: 'بدأ توليد المجسم بنجاح في الخلفية!' 
    });

  } catch (error: any) {
    return res.status(500).json({ success: false, error: error.message });
  }
}
