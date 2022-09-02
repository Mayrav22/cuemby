<script>
import { RouterLink, RouterView } from 'vue-router'
import gql from 'graphql-tag'

export default {
  data() {
    return {
      players: [],
      club: null
    }
  },
  apollo: {
    getPlayers: {
      query: gql`query getPlayers($club: String) {
        getPlayers(club: $club) {
          players {
            id
            name
            position
            club
            nation
            idFut
          }
        }
      }`,
      variables() {
        return {
          club: this.club
        }
      },
      result(response) {
        this.players = response.data.getPlayers.players
      }
    }
  }
}
</script>

<template>
  <div class="bg-gray-100 min-h-screen flex justify-center items-center">
    <div class="w-3/6 bg-white h-96 rounded-lg p-5 shadow-lg">
      <div class="search">
        <label for="club">
          Busque por su club favorito:
        </label>
        <input v-model="club" placeholder="Ingrese club.." class="ml-3 input-custom border border-gray-300 py-1 px-2 rounded-md w-1/2 focus:border-cyan-300 focus:shadow-teal-400  " />
      </div>

      <div class="mt-4">
        <h2 class="text-xl font-medium">Jugadores {{club ? `del club ${club}` : ''}} </h2>
      </div>


      <div class="overflow-auto h-72 grid grid-cols-2 gap-4">
        
        <div class=" m-4 flex border shadow-md hover:cursor-pointer transition ease-in-out delay-150 hover:-translate-y-1 hover:scale-110 duration-300" v-for="player,i in players" :key="i">
          <div class="img">
            <img :src="`https://upload.wikimedia.org/wikipedia/commons/thumb/b/b6/Juan_Cuadrado_2019_%28cropped%29.jpg/225px-Juan_Cuadrado_2019_%28cropped%29.jpg`" class="w-12 h-13" />
          </div>
          <div class="mx-2">
            <p> <b>Name:</b> {{player.name}}</p> 
            <p> <b>Position:</b> {{player.position}}</p> 
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style>
.input-custom:focus {
    color: #212529;
    background-color: #fff;
    border-color: #86b7fe;
    outline: 0;
    box-shadow: 0 0 0 0.25rem rgb(13 110 253 / 25%);
}
</style>