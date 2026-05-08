import Latex from "../../utils/diplay_latex";

export default function EpipolarLines() {
  const baseUrl = import.meta.env.BASE_URL;

  return (
    <section id="epipolar-lines" className="scroll-mt-24">
      <h1 className="mb-4 text-3xl font-bold text-red-400">Epipolar Lines</h1>
      <h1 className="mb-4 text-md font-bold text-red-300 ">Notation and Setup</h1>




      <img
        className="block w-[75%] mx-auto"
        src={`${baseUrl}images/epipolor_gemoetry_unaligned_cameras.svg`}
      />
      <img
        className="block w-[75%] mx-auto"
        src={`${baseUrl}images/epipolor_gemoetry_aligned_cameras.svg`}
      />

    </section>
  );
}
