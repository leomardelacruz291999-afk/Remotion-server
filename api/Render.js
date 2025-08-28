import { bundle } from "@remotion/bundler";
import { renderMedia } from "@remotion/renderer";
import path from "path";

export default async function handler(req, res) {
  if (req.method !== "POST") {
    return res.status(405).json({ error: "Only POST allowed" });
  }

  try {
    const { title, script, audio_url, image_url } = req.body;
    const entry = path.join(process.cwd(), "remotion", "Root.jsx");

    const bundled = await bundle(entry);
    const outputLocation = `/tmp/output-${Date.now()}.mp4`;

    await renderMedia({
      composition: "CookingVideo",
      serveUrl: bundled,
      codec: "h264",
      outputLocation,
      inputProps: { title, script, audio_url, image_url },
    });

    res.setHeader("Content-Type", "application/json");
    res.status(200).json({
      video_url: `https://${req.headers.host}/api/files/${outputLocation}`,
    });
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: "Render failed" });
  }
}
