import { Image, Pressable, StyleSheet, Text, View } from "react-native"
import Hr from "./Hr"

const styles = StyleSheet.create({
    text: {
        fontFamily: 'Sansita',
        fontSize: 32
    },
    icon: {
        width:40,
        height:40,
        marginHorizontal:5
    }
})

export default props => {
    return (
        <View style={{alignSelf:"stretch"}}>
            <View style={{height:80, alignSelf: "stretch", justifyContent: "space-between", marginHorizontal: 25, paddingTop: 10, flexDirection: "row", alignItems: "center"}}>
                <Text style={styles.text}>{props.text}</Text>
                <View style={{flexDirection:"row"}}>
                    <Image style={styles.icon} source={require("../assets/Notifications.png")} />
                </View>
            </View>
            <Hr/>
        </View>
    )
}