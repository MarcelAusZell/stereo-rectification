
export default function Intro() {
  const baseUrl = import.meta.env.BASE_URL;

  return (
    <section id="introduction" className="scroll-mt-24">
      <h1 className="mb-4 text-3xl font-bold text-red-400">Introduction</h1>

      In this Tutorial I explain how to implement Stereo Rectification from scratch.
      Stereo rectification is a preprocessing step in stereo vision where two images from different camera viewpoints are
      transformed so that corresponding points lie on the same horizontal line.

      After rectification:
      <ul className="list-disc pl-6 mt-3 mb-3">
        <li>
          a point in the left image and its matching point in the right image have the same y-coordinate
        </li>
        <li>
          disparity becomes purely horizontal
        </li>
        <li>
          correspondence search changes from a 2D search to a 1D search
        </li>
      </ul>


      This makes stereo matching much simpler and faster.

      <img
        className="block w-[80%] mx-auto mt-10"
        src={`${baseUrl}images/stereo_rectification.svg`}
      />
    </section>
  );
}
