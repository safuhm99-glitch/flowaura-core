import type { NextApiRequest, NextApiResponse } from 'next';

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  const { taskId } = req.query;

  if (!taskId) {
    return res.status(400).json({ success: false, error: 'مطلوب رقم الطلب taskId' });
  }

  try {
    const response = await fetch(`https://api.meshy.ai/v2/text-to-3d/${taskId}`, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${process.env.MESHY_API_KEY}`,
      },
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.message || 'فشل في جلب حالة الطلب من Meshy AI');
    }

    if (data.status === 'SUCCEEDED') {
      return res.status(200).json({
        success: true,
        status: 'completed',
        modelUrl: data.model_urls?.glb || data.model_url, 
        thumbnailUrl: data.thumbnail_url 
      });
    } else if (data.status === 'FAILED') {
      return res.status(200).json({
        success: true,
        status: 'failed',
        error: data.task_error?.message || 'فشل توليد المجسم'
      });
    } else {
      return res.status(200).json({
        success: true,
        status: 'processing',
        progress: data.progress || 0
      });
    }

  } catch (error: any) {
    return res.status(500).json({ success: false, error: error.message });
  }
}
