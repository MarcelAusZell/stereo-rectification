import { InlineMath, BlockMath } from "react-katex";

export default function Latex({ children, block = false }) {
  const content = typeof children === "string"
    ? children
    : String(children);

  return block
    ? <BlockMath math={content} />
    : <InlineMath math={content} />;
}