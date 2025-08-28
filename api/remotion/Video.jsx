import { Audio, Img, Sequence, useVideoConfig } from "remotion";

export const Video = ({ title, script, audio_url, image_url }) => {
  return (
    <>
      <Sequence from={0}>
        <Img src={image_url} style={{ width: "100%", height: "100%" }} />
      </Sequence>
      <Sequence from={30}>
        <h1 style={{ color: "white", fontSize: 60, textAlign: "center" }}>
          {title}
        </h1>
      </Sequence>
      <Audio src={audio_url} />
    </>
  );
};
