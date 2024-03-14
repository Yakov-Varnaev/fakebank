<template>
  <div class="d-flex flex-column justify-space-between fill-height">
    <v-container>
      <slot name="content"></slot>
    </v-container>
    <v-container>
      <v-col cols="12">
        <slot name="pagination"></slot>
      </v-col>
    </v-container>
  </div>
</template>
