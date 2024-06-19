import json
import aiohttp
import requests


async def async_stream_response(url, headers, data):
    """
        VLLM 출력 시 asynchronize 하게 print할 수 있도록 구현한 함수입니다. 
        chat_comp_response에서 인자 streaming을 True로 전달하면 해당 함수가 호출됩니다.
    """
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=data) as response:
            response.raise_for_status()
            
            async for line in response.content:
                try:
                    decoded_line = line.decode('utf-8').strip()
                    if decoded_line.startswith("data: "):
                        json_data = json.loads(decoded_line.split('data: ')[1])
                        chunk = json_data.get('choices', [])[0].get('delta', {}).get('content', '')
                        yield chunk
                
                except ValueError:
                    yield '\n'
                except Exception as e:
                    print('\n', e)


def stream_response(url, headers, data):
    import time
    with requests.post(url, headers=headers, json=data) as response:
        response.raise_for_status()
        
        for _chunk in response.iter_lines(chunk_size=32):# chunk_size=1,
                                            # decode_unicode=False,
                                            # delimiter=b"\0"):
            if _chunk:
                try:
                    decoded_line = _chunk.decode('utf-8').strip()
                    if decoded_line.startswith("data: "):
                        # print(decoded_line)
                        json_data = json.loads(decoded_line.split('data: ')[1])
                        chunk = json_data.get('choices', [])[0].get('delta', {}).get('content', '')
                        time.sleep(0.003)
                        yield chunk
                except Exception as e:
                    print('\n', e)
                