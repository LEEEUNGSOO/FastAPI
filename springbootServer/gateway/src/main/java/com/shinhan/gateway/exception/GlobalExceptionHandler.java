package com.shinhan.gateway.exception;

import java.nio.charset.StandardCharsets;
import java.util.Map;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;
import org.springframework.web.client.HttpClientErrorException;
import org.springframework.web.client.ResourceAccessException;

@RestControllerAdvice                                    // 모든 컨트롤러의 예외를 여기서 받음
public class GlobalExceptionHandler {

    // ① FastAPI에 연결 자체가 안 될 때 (꺼져 있음, 타임아웃) → 503
    @ExceptionHandler(ResourceAccessException.class)
    public ResponseEntity<Map<String, String>> fastApiDown(ResourceAccessException e) {
        return ResponseEntity.status(HttpStatus.SERVICE_UNAVAILABLE)
                .body(Map.of("message", "분석 서버(FastAPI)에 연결할 수 없습니다."));
    }

    // ② FastAPI가 4xx(404, 422 ...)를 줄 때 → 상태 코드와 본문을 그대로 전달
    @ExceptionHandler(HttpClientErrorException.class)
    public ResponseEntity<String> fastApiClientError(HttpClientErrorException e) {
        return ResponseEntity.status(e.getStatusCode())                                    // 404면 404
                .contentType(new MediaType(MediaType.APPLICATION_JSON, StandardCharsets.UTF_8))
                .body(e.getResponseBodyAsString(StandardCharsets.UTF_8));                // 한글 안 깨지게
    }
}

/* ===== 전체 이해 =====
 * - 서버가 둘이면 "상대가 없을 때"와 "상대가 에러를 줄 때"를 대비해야 합니다.
 * - 이 클래스가 없으면 두 경우 모두 Postman에는 500만 보입니다.
 *     FastAPI 꺼짐   ResourceAccessException  → 503 {"message":"분석 서버(FastAPI)에 연결할 수 없습니다."}
 *     없는 계좌     HttpClientErrorException → 404 {"detail":"계좌를 찾을 수 없습니다: A009"}
 *     FastAPI 5xx     HttpServerErrorException → (오늘은 안 잡음) 500
 * - 예외 "종류"로 잡기 때문에 로그 메시지 끝이 Connection refused 든 null 이든 똑같이 503
 * - 실무에서는 FastAPI 본문을 그대로 내보내지 않고 한 번 감쌀 (내부 정보 숨김). 오늘은 흐름 확인용
 */