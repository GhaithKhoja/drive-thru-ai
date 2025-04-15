<script lang="ts">
import Button from '$lib/components/ui/button/button.svelte';
import { onMount } from 'svelte';

let counts = {
  burgers: 0,
  fries: 0,
  drinks: 0
};

let orderHistory: { id: number; burgers: number; fries: number; drinks: number; message: string; }[] = [];
let nextOrderId = 1;

let chatMessage = '';

async function runMessage() {
  if (!chatMessage.trim()) return;

  try {
    const response = await fetch('http://127.0.0.1:8000/generate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ prompt: chatMessage })
    });
    const json = await response.json();
    const data = json.response;

    // Handle deletes first
    if (data.deleteOrder && Array.isArray(data.deleteOrder.order_ids)) {
      // Now treat order_ids as actual order ids
      const deleteIds = data.deleteOrder.order_ids;
      for (const id of deleteIds) {
        const index = orderHistory.findIndex(order => order.id === id);
        if (index !== -1) {
          counts.burgers -= orderHistory[index].burgers;
          counts.fries -= orderHistory[index].fries;
          counts.drinks -= orderHistory[index].drinks;
          orderHistory = orderHistory.filter((_, i) => i !== index);
        }
      }
    }

    // Handle addOrder
    if (data.addOrder) {
      const { burger_count, fries_count, drink_count } = data.addOrder;
      const newOrder = {
        id: nextOrderId++,
        burgers: burger_count,
        fries: fries_count,
        drinks: drink_count,
        message: chatMessage
      };
      orderHistory = [...orderHistory, newOrder];
      counts.burgers += burger_count;
      counts.fries += fries_count;
      counts.drinks += drink_count;
    }

    if (!data.addOrder && !data.deleteOrder) {
      alert('Unknown response from backend.');
    }
  } catch (err) {
    alert('Failed to contact backend.');
    console.error(err);
  }
  chatMessage = '';
}
</script>

<div class="px-32 flex flex-col items-center">

    <!-- Total counts -->
    <div class="flex gap-8 justify-center items-center mt-16">
        {#each Object.entries(counts) as [item, value]}
            <div class="bg-white shadow-lg rounded-xl p-8 flex flex-col items-center justify-between">
                <h2 class="text-2xl font-bold capitalize">Total # of {item}</h2>
                <div class="text-5xl mt-8">{value}</div>
            </div>
        {/each}
    </div>

    <!-- Chat input box -->
    <div class="w-full flex justify-center mt-16">
        <div class="flex gap-2 w-full max-w-xl items-center">
        <input
            class="flex-1 border border-gray-300 rounded-lg px-4 py-3 text-lg focus:outline-none focus:ring-2 focus:ring-primary"
            type="text"
            bind:value={chatMessage}
            placeholder="Drive thru message"
        />
        <Button size="lg" variant="default" on:click={runMessage}>Run</Button>
        </div>
    </div>

    <!-- Order History Section -->
    <div class="w-full flex flex-col items-center mt-16">
      <h2 class="text-2xl font-bold mb-4">Order History</h2>
      {#if orderHistory.length === 0}
        <div class="text-gray-500">No orders yet.</div>
      {:else}
        <div class="w-full max-w-2xl text-center">
          <div class="grid grid-cols-4 gap-4 font-semibold border-b pb-2 mb-2">
            <div>Order #</div>
            <div>Burgers</div>
            <div>Fries</div>
            <div>Drinks</div>
          </div>
          {#each orderHistory as order}
            <div class="grid grid-cols-4 gap-4 py-2 border-b items-center">
              <div>{order.id}</div>
              <div>{order.burgers}</div>
              <div>{order.fries}</div>
              <div>{order.drinks}</div>
            </div>
          {/each}
        </div>
      {/if}
    </div>
</div>
