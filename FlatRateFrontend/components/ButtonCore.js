// Components in react native are, essentially, 
// reusable, useful bits of JSX 

// this one is used whenever we need a button to press

import { Image, Pressable, StyleSheet, Text } from "react-native"
import colors from "../colors";

const styles = StyleSheet.create({
    core: {
        borderWidth: 2,
        borderBottomWidth: 4,
        borderRightWidth: 4,
        borderColor: colors.purple,
        borderRadius: 10,
        justifyContent: "center",
        alignItems: 'center',
        flexDirection: "row"
    },
    text: {
        fontFamily: "Sansita"
    },
    icon: {
        width:30,
        height:30,
        marginLeft: 5
    }
})

export default (props) => {
    return (
        <Pressable onPress={props.onPress} style={[styles.core, props.style, {backgroundColor: props.bgColor}]}>
            <Text style={[styles.text, {color: props.fgColor, fontSize: props.size}]}>{props.text}</Text>
            { props.image ? <Image style={[styles.icon]} source={props.image} /> : null }
        </Pressable>
    )
}