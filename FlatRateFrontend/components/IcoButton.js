import { Pressable, StyleSheet, Text, Image } from "react-native";
import colors from "../colors";
import fonts from "../fonts";

const styles = StyleSheet.create({
    container: {
        backgroundColor: colors.white,
        borderRadius: 10,
        borderWidth: 2,
        borderBottomWidth:4,
        borderRightWidth:4,
        borderColor: colors.purple,
        paddingHorizontal:20,
        paddingVertical: 10,
        marginVertical:6,
        flexDirection: "row",
        alignItems: "center",
        justifyContent: "space-between"
    },
    active: {
        backgroundColor: colors.blue
    },
    text: {
        fontFamily: fonts.prompt,
        fontSize: 23,
        textAlign:"left"
    },
    icon: {
        width:40,
        height:40,
        // marginLeft:30
    }
})

export default props => {
    return (
        <Pressable style={[styles.container, props.active && styles.active]} onPress={props.onPress}>
            <Text style={styles.text}>{props.text}</Text>
            <Image style={styles.icon} source={props.image}/>
        </Pressable>
    )
}