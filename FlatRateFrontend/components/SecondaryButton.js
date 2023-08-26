import colors from "../colors"
import ButtonCore from "./ButtonCore"

// secondary buttons are just a stylistic extension of button core

export default (props) => {
    return (
        <ButtonCore {...props} bgColor={colors.white} fgColor={colors.orange} />
    )
}