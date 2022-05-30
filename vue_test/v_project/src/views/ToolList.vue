<template>
    <div id="app">
        数学：<input type="text" v-model='math_score'><br>
        英语：<input type="text" v-model='english_score'><br>
        总得分(函数-单向绑定)：<input type="text" v-model='sumScore'><br>
        
        总得分（计算属性-单向绑定）：<input type="text" v-model='sumScore1'><br>
        
        总得分（计算属性-双向绑定）：<input type="text" v-model='sumScore2'><br>

        
        总得分（监听器）：<input type="text" v-model='sumScore3'>

    </div>
</template>


<script>
        // 1.函数没有缓存，每次都会被调用
        // 2.计算属性有缓存，只有当计算属性体内的属性值被更改后才会被调用
        // 3.函数只支持单向绑定
        // 4.计算属性默认情况下，只有getter函数，而没有setter函数，所以只支持单向，如果要进行双向绑定，则需要自定义setter函数
        var vm = new Vue({
            el:'#app',
            data() {
                return {
                    math_score:85,
                    english_score:90,
                    sumScore3:0 //通过监听器，计算出来的总得分
                }
            },
            methods: {
                sumScore:function(){
                    console.log('score函数被调用')
                    return (this.math_score-0) + (this.english_score-0)
                    // （num-0）将字符串转换为数字计算，而不是字符串的拼接
                }
            },
            computed: { //定义计算属性选项
                // 这个是单向绑定，默认只有getter方法
                sumScore1:function(){
                    // 计算属性有缓存，如果计算属性体内的属性值没有发生改变，则不会从新计算
                    console.log('score1函数被调用')
                    return (this.math_score-0) + (this.english_score-0)
                },
                sumScore2:{ //有了setter和getter后就可以进行双向绑定
                    // 获取数据
                    get:function(){
                        console.log('score2.get函数被调用')
                        return (this.math_score-0) + (this.english_score-0) 
                    },
                    // 设置数据,当计算属性更新之后会调用set方法
                    set:function(newValue){ 
                        // newValue是sumScore2更新之后的新值
                        console.log('score2.set函数被调用')
                        var avgScore = newValue / 2
                        this.math_score = avgScore
                        this.english_score = avgScore
                    }
                }
            },
            // 监听器
            watch: {
                // 需求：通过watch选项监听数学分数，当数学更新后回调函数中重新计算总分sumScore
                math_score:function(newValue,oldValue){
                    console.log('watch监听到了数学分数已经更新')
                    this.sumScore3=(newValue-0) + (this.english_score-0)
                }
            },
        })

        vm.$watch('english_score', function(newValue){
            console.log('watch监听到了英语分数已经更新')
            this.sumScore3=(newValue-0) + (this.english_score-0)
        })
</script>


<style scoped>

</style>
