<template>
  <section class="is-transparentbackground">
      <span v-if="show" class="justify-center d-flex">

          <v-btn
          class="mr-10"
          fab
          dark
          x-small
          outlined
          color="secondary"
          v-on:click="goToEditQuestion">
            <v-icon dark>mdi-arrow-left</v-icon>
          </v-btn>

          <v-btn
          small
          color="primary"
          dark
          v-if="typeof highlitedText === 'string' && highlitedText.length < 200"
          v-on:click="onClick"
          >Valider
          </v-btn>

          <v-btn
          small
          disabled
          v-else
          >Valider
          </v-btn>
      </span>
  </section>
</template>

<style scoped>
.paddingright{
  padding-right: 15px !important;
}
.has-text-left{
  justify-content: end;
}
.has-background-royalblue{
  background-color:royalblue !important;
}
</style>

<script>
import { mapState } from 'vuex'

export default {
  computed: {
    ...mapState([
      'highlitedText',
      'editMode'
    ]),
    show(){
      return !this.$store.getters.hasAnswer && this.editMode == false
    },
  },

  methods: {
    onClick(){
      this.$store.dispatch('addNewHighlitedText')
      this.$store.commit('setshowContinue',true)
    },

    goToEditQuestion(){
      this.$store.commit('setEditeMode',true)
    }

  },

}
</script>
