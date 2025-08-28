import { Composition } from "remotion";
import { Video } from "./Video";

export const RemotionRoot = () => (
  <Composition
    id="CookingVideo"
    component={Video}
    durationInFrames={1800} // 1 min @ 30fps
    fps={30}
    width={1280}
    height={720}
  />
);
