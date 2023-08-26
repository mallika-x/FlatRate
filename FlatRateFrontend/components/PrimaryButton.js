import colors from "../colors"
import ButtonCore from "./ButtonCore"

// primary buttons are an extension of button core

export default (props) => {
    return (
        <ButtonCore {...props} bgColor={props.disabled ? colors.grey : colors.orange} fgColor={colors.white} />
    )
}