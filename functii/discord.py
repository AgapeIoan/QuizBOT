import disnake

async def disable_button(buton_fain):
    buton_fain.disabled = True
    buton_fain.style = disnake.ButtonStyle.gray
