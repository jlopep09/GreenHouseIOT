import React from 'react'

export const ThemeButton = () => {
  return (
    <div className="dropdown">
        <div tabIndex={0} role="button" className="btn btn-ghost m-1">
            Theme
            <ArrowSVG/>
        </div>
        <ul className="dropdown-content bg-base-300 rounded-box z-1 w-52 p-2 shadow-2xl">
            <ThemeItem theme={"default"} label={"Default"}/>
            <ThemeItem theme={"retro"} label={"Retro"}/>
            <ThemeItem theme={"cyberpunk"} label={"Cyberpunk"}/>
            <ThemeItem theme={"valentine"} label={"Valentine"}/>
            <ThemeItem theme={"aqua"} label={"Aqua"}/>
            <ThemeItem theme={"dark"} label={"Dark"}/>
            <ThemeItem theme={"light"} label={"Light"}/>
            <ThemeItem theme={"halloween"} label={"Halloween"}/>
            <ThemeItem theme={"forest"} label={"Forest"}/>
            <ThemeItem theme={"abyss"} label={"Abyss"}/>
        </ul>
    </div>
  )
}
const ThemeItem = ({theme, label}) => {
    return(
        <li>
            <input
                type="radio"
                name="theme-dropdown"
                className="theme-controller w-full btn btn-sm btn-ghost justify-start"
                aria-label={label}
                value={theme} />
        </li>
    )
}
export const ArrowSVG = () => {
    return(
        <svg
            width="12px"
            height="12px"
            className="inline-block h-2 w-2 fill-current opacity-60"
            xmlns="http://www.w3.org/2000/svg"
            viewBox="0 0 2048 2048">

            <path d="M1799 349l242 241-1017 1017L7 590l242-241 775 775 775-775z"></path>
        </svg>
    )
}
