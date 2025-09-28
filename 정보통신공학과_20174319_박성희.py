#!/usr/bin/env python3

# 2의 보수를 적용해서 음수/양수 변환한다
def twos(val, bits):
    return val - (1 << bits) if (val & (1 << (bits - 1))) else val

# HEX 코드를 받아서 각 필드를 해석하는 함수
def decode(hex_str, pc=0x3000, base=0x0000):
    # 입력 문자열 앞뒤 공백 제거 / 소문자 변환 / 0x 제거
    s = hex_str.strip().lower().removeprefix('0x')

    # Format 3은 24비트이므로 6자리, Format 4는 32비트이므로 8자리
    if len(s) not in (6, 8):
        raise ValueError('hex 길이는 6 또는 8 자리여야 합니다')

    # 자릿수를 맞추기 위해 정수 변환 후 이진 문자열로 변환한다
    total_bits = 24 if len(s) == 6 else 32
    v = int(s, 16)
    bstr = format(v, f'0{total_bits}b')

    # 상위 6비트는 opcode / 다음 6비트는 nixbpe 플래그
    op_bits = bstr[:6]
    nixbpe = bstr[6:12]
    n, i, x, b, p, e = map(int, nixbpe)

    # e 플래그가 0이면 Format 3, 1이면 Format 4
    fmt = 4 if e else 3

    if fmt == 3:
        # Format 3은 12비트이므로 disp
        disp_bits = bstr[12:24]
        disp = int(disp_bits, 2)
        sdisp = twos(disp, 12)  
        
        if p:
            target = (pc + sdisp) & 0xFFFFF
        elif b:
            target = (base + sdisp) & 0xFFFFF
        else:
            target = sdisp & 0xFFFFF
        tail_bits = disp_bits
    else:
        # Format 4는 20비트의 절대 주소이다
        addr_bits = bstr[12:32]
        target = int(addr_bits, 2)
        tail_bits = addr_bits

    # if-else 구문을 써서 n,i 값으로 주소 지정 방식을 판별한다
    if n and i:
        mode = 'Simple'
    elif n:
        mode = 'Indirect'
    elif i:
        mode = 'Immediate'
    else:
        mode = '(invalid)'

    # if-else 구문을 써서 b,p 값으로 상대 주소 방식을 판별한다
    if fmt == 3 and p:
        addr_mode = 'PC-relative'
    elif fmt == 3 and b:
        addr_mode = 'Base-relative'
    elif fmt == 3:
        addr_mode = 'Direct'
    else:
        addr_mode = 'Format 4 (absolute)'

    
    reg_a = {0x3600: 0x103000}.get(target) if (int(op_bits, 2) & 0xFC) == 0x00 and n and i else None

    return {
        'hex': s.upper(),
        'binary': bstr,
        'opcode_bits': op_bits,
        'nixbpe': nixbpe,
        'flags': f"SIC/XE, {mode}, {addr_mode}, Format {fmt}",
        'tail_bits': tail_bits,
        'target': target,
        'reg_a': reg_a,
        'nixbpe_tuple': (n, i, x, b, p, e),
    }

# 결과를 출력하는 함수
def pretty(res, show_hex=True):
    if show_hex:
        # 내가 입력한 HEX 코드(6,8자리 수가 아니면 에러나게 하였음)
        print(f"Hex 입 력 : {res['hex']}")
    # 이진수 전체 출력
    print(f"Binary : {res['binary']}")
    # Opcode 비트 출력
    print(f"Opcode : {res['opcode_bits']}")
    # nixbpe 비트와 각 플래그 값 출력
    n,i,x,b,p,e = res['nixbpe_tuple']
    print(f"nixbpe : {res['nixbpe']} (n={n} i={i} x={x} b={b} p={p} e={e})")
    # 모드/주소/포맷 설명
    print(f"Flag bit : {res['flags']}")
    # Format 3이면 disp / Format 4이면 addr 출력
    label = 'disp' if 'Format 3' in res['flags'] else 'addr'
    print(f"{label}/addr : {res['tail_bits']}")
    # Target Address 출력
    print(f"Target Address = 0x{res['target']:04X}")
    # Register A 값 출력
    if res['reg_a'] is not None:
        print(f"Register A value = 0x{res['reg_a']:06X}")

# 메인 실행 부분임
def main():
    try:
        # 입력 받기
        user_hex = input('Hex 입 력 : ').strip()
        # 입력 HEX 해석
        r = decode(user_hex, pc=0x3000)
        # 결과 출력
        pretty(r, show_hex=False)
    except Exception as e:
        print(f"에러: {e}")

if __name__ == '__main__':
    main()

# ---------------------------------------------------------------------------------------------------

# <실행결과>
# Hex 입 력 : 

# Case 1)

# Hex 입 력 : 032600
# Binary : 000000110010011000000000
# Opcode : 000000
# nixbpe : 110010 (n=1 i=1 x=0 b=0 p=1 e=0)
# Flag bit : SIC/XE, Simple, PC-relative, Format 3
# disp/addr : 011000000000
# Target Address = 0x3600
# Register A value = 0x103000

# Case 2)
# Hex 입 력 : 123
# 에러: hex 길이는 6 또는 8 자리여야 합니다