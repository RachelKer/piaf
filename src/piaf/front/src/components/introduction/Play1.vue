<template>
  <v-app>
  <v-app-bar app hide-on-scroll>
    <NavbarProfile :NavbarTitle="NavbarTitle"/>
  </v-app-bar>
  <v-content>
    <v-container fluid>
      <v-container class="maxWid700">
        <Play1content
          v-bind:question="test.question"
          v-bind:text="test.text"
          :key="test.step"
        />
      </v-container>
    </v-container>
    <Animation/>
  </v-content>
  <v-footer
  style="z-index:10"
  padless
  fixed
  min-height='150px'
  :class="show && test.answer == test.exp ? 'ligthG' :
  show && test.answer != test.exp ? 'ligthR' : 'white'">
      <div style="min-height: 4px;min-width:100%;position:absolute;top:0px;">
        <v-progress-linear
        :value="(!networkIssueMessage) ? step / tests.length * 100 : 100"
        color="blue lighten-2"
        height=8
        ></v-progress-linear>
      </div>
    <v-flex xs12 my-0 justify-center class="container" v-if="!show">

      <PlayFooterTitle
      :title="`Est-ce une question pertinente ?`"
      :networkIssueMessage="networkIssueMessage"/>

      <PlayFooterLoading
      :loading="loading"
      :networkIssueMessage="networkIssueMessage"
      v-on:resubmit="submitAnswers"/>

      <v-row class="maxWid700 mx-auto" v-if="!loading && !networkIssueMessage">
        <v-col cols='12' class="pr-0 textContainer">
          <span class="btnContainer">
            <v-btn
            class="mx-2"
            fab
            dark
            small
            outlined
            color="error"
            v-on:click="onClick(false)">
              <v-icon dark>mdi-close</v-icon>
            </v-btn>
            <span class="error--text">NON</span>
          </span>
          <span class="btnContainer">
            <v-btn
            class="mx-2"
            fab
            dark
            small
            outlined
            color="success"
            v-on:click="onClick(true)">
              <v-icon dark>mdi-check</v-icon>
            </v-btn>
            <span class="success--text">OUI</span>
          </span>
        </v-col>
      </v-row>
    </v-flex>

    <v-flex xs12 my-0 justify-center class="container" v-else>
      <v-row class="maxWid700 mx-auto">
        <v-col cols='12' class="pr-0 textContainer bold" style="color:green" v-if="test.answer == test.exp">
          {{test.explainP}}
        </v-col>
        <v-col cols='12' class="pr-0 textContainer bold" style="color:red" v-else>
          {{test.explainN}}
        </v-col>
      </v-row>

      <span>
        <v-row class="maxWid700 mx-auto textContainer">
          <v-col cols='12' class="pr-0 textContainer">
            <v-btn
            small
            :color="test.answer == test.exp ? 'success' : 'error'"
            dark
            class="alignSelf"
            v-on:click="onClickContinue()">continuer
            </v-btn>
          </v-col>
        </v-row>
      </span>

    </v-flex>
  </v-footer>
  </v-app>
</template>

<script>
import Play1content from '../../components/introduction/Play1content';
import PlayFooterLoading from '../../components/introduction/PlayFooterLoading';
import PlayFooterTitle from '../../components/introduction/PlayFooterTitle';
import Animation from '../Animation.vue';
import NavbarProfile from '../../components/NavbarProfile';
import {playMixin} from './mixin.js';

export default {
  mixins: [playMixin],
  data: () => ({
    step: 0,
    show:false,
    tests: [
      {
        step : 2,
        exp : true,
        question : "Quel est le tome de Tintin marquant le début de la saga ?",
        text : "Dès le premier album, Tintin au pays des Soviets, Tintin est un reporter travaillant pour Le Petit Vingtième, le journal publiant ses aventures.",
        explainP: "Bonne réponse !",
        explainN: "La bonne solution était : OUI"
      },
      {
        step : 3,
        exp : false,
        question : "Quel est le premier album de Tintin ?",
        text : "Dès le premier album, Tintin au pays des Soviets, Tintin est un reporter travaillant pour Le Petit Vingtième, le journal publiant ses aventures.",
        explainP: "Bonne réponse !",
        explainN: "La bonne solution était : NON"
      },
      {
        step : 0,
        exp : false,
        question : "Qui est reporter pour un journal belge ?",
        text : "Tintin est un reporter dans un journal belge.",
        explainP: "Bonne réponse !",
        explainN: "La bonne solution était : NON"
      },
      {
        step : 1,
        exp : true,
        question : "Qui est journaliste ?",
        text : "Tintin est un reporter dans un journal belge.",
        explainP: "Bonne réponse !",
        explainN: "La bonne solution était : OUI"
      },
      {
        step : 4,
        exp : true,
        question : "Quel est le nom de la gazette dont est issu Tintin ?",
        text : "Dès le premier album, Tintin au pays des Soviets, Tintin est un reporter travaillant pour Le Petit Vingtième, le journal publiant ses aventures.",
        explainP: "Bonne réponse !",
        explainN: "La bonne solution était : OUI"
      }
    ]
  }),
  components: {
    Play1content,
    PlayFooterLoading,
    PlayFooterTitle,
    Animation,
    NavbarProfile,
  },
  computed:{
    toNiveau(){
      return "/introduction/"+Number(this.$route.params.level)+"/play"
    },
    NavbarTitle () {
      return 'Niveau ' + this.$route.params.level
    },
    test() {
      const findIdFunction = (obj) => obj.step == this.step;
      let index = this.tests.findIndex(findIdFunction);
      return this.tests[index]
    },
    isLastStep() {
      return this.step + 1 === this.tests.length
    },
  },
  methods:{
    async onClick(boo){
      const findIdFunction = (obj) => obj.step == this.step;
      let index = this.tests.findIndex(findIdFunction);
      this.tests[index].answer = boo
      this.show = !this.show
    },
    async onClickContinue(){
      this.show = !this.show
      if (this.isLastStep) {
        await this.submitAnswers()
      } else {
        this.step++
      }
    },
    async submitAnswers(){
      this.loading = true
      let score = this.tests.reduce((acc,obj) => (obj.answer == obj.exp) ? acc+1 : acc,0)
      score = 100 * score / this.tests.length
      let scoreUpdate = await this.sendScore(score,1)
      this.loading = false
      if (scoreUpdate) {
        this.$router.push('/introduction/'+this.$route.params.level+'/bravo')
      } else {
        this.networkIssueMessage = true
      }
    },
  }
};
</script>

<style scoped>
.btnContainer{
  display: flex;
  justify-content: space-around;
  flex-direction: column;
  text-align: center;
}
.ligthG{
  background-color: #c7e6b0 !important
}
.ligthR{
  background-color: #ffc1c1 !important
}
</style>
