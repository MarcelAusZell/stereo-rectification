export default function DisplayImage({
  path = "",
  width,
}) {
  const base = import.meta.env.BASE_URL

  return (
    <div className="flex justify-center select-none pointer-events-none">
      <img
        src={`${base}${path}`}
        alt=""
        draggable="false"
        loading="lazy"
        decoding="async"
        className={width ? undefined : "w-full"}
        style={width ? { width } : undefined}
        
      />
    </div>
  )
}