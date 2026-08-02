# frozen_string_literal: true

# Lectura de dimensiones de imagen sin dependencias: parsea encabezados
# WebP (VP8/VP8L/VP8X), PNG y JPEG con solo stdlib de Ruby.
#
# Extraído de verify_distribution_readiness.rb, que solo necesitaba el ancho.
# verify_visual_assets.rb necesita también el alto para contrastar las
# dimensiones declaradas en _data/visuales/<slug>.yml contra el archivo real.
#
# No cubre SVG a propósito: no tiene encabezado binario y sus dimensiones
# dependen de width/height o viewBox, que pueden estar en unidades relativas.
# Quien lo llame debe tratar el nil de un .svg como "no verificable", no como error.

# Devuelve [ancho, alto] o nil si el formato no se reconoce o el archivo no existe.
def image_dimensions(path)
  return nil unless File.file?(path)

  bytes = File.open(path, "rb") { |f| f.read(64) }
  return nil unless bytes

  if bytes[0, 4] == "RIFF" && bytes[8, 4] == "WEBP"
    webp_dimensions(bytes)
  elsif bytes[0, 8] == "\x89PNG\r\n\x1a\n".b
    [bytes[16, 4].unpack1("N"), bytes[20, 4].unpack1("N")]
  elsif bytes[0, 2] == "\xFF\xD8".b
    jpeg_dimensions(path)
  end
rescue StandardError
  nil
end

# Compatibilidad con el uso original en verify_distribution_readiness.rb.
def image_width(path)
  image_dimensions(path)&.first
end

def webp_dimensions(bytes)
  case bytes[12, 4]
  when "VP8 "
    # Lossy: ancho y alto son little-endian 14-bit en los bytes 26-29.
    w = bytes[26, 2].unpack1("v") & 0x3FFF
    h = bytes[28, 2].unpack1("v") & 0x3FFF
    (w.positive? && h.positive?) ? [w, h] : nil
  when "VP8L"
    # Lossless: 14 bits de ancho y 14 de alto, menos uno, empaquetados en 32 bits.
    b = bytes[21, 4].unpack1("V")
    [(b & 0x3FFF) + 1, ((b >> 14) & 0x3FFF) + 1]
  when "VP8X"
    # Extendido: canvas menos uno, 24-bit little-endian (ancho en 24-26, alto en 27-29).
    [le24(bytes[24, 3]) + 1, le24(bytes[27, 3]) + 1]
  end
end

def le24(chunk)
  chunk.bytes.reverse.inject(0) { |acc, b| (acc << 8) | b }
end

def jpeg_dimensions(path)
  File.open(path, "rb") do |f|
    f.read(2)
    loop do
      marker = f.read(2)
      break unless marker && marker[0] == "\xFF".b

      code = marker[1].unpack1("C")
      break if code == 0xD9

      length = f.read(2)&.unpack1("n")
      break unless length

      # SOFn lleva las dimensiones, salvo DHT (C4), JPG (C8) y DAC (CC).
      if (0xC0..0xCF).cover?(code) && ![0xC4, 0xC8, 0xCC].include?(code)
        f.read(1)
        height, width = f.read(4).unpack("nn")
        return [width, height]
      else
        f.read(length - 2)
      end
    end
  end
  nil
end
