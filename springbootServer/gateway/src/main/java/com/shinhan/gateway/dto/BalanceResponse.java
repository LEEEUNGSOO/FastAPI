package com.shinhan.gateway.dto;



// FastAPI Balance 모델과 짝. 필드 이름 = JSON 키 이름
public record BalanceResponse(String accountId, String ownerName, Long balance) {}

/* ===== 전체 이해 =====
 * - FastAPI 응답 {"accountId":"A001","ownerName":"김신한","balance":5230000} 을 담는 그릇
 * - record = 필드·생성자·getter·equals를 한 줄로 만드는 불변 DTO (Java 16+)
 * - Jackson이 이름으로 짝을 찾음 → 이름이 다르면 에러 없이 null
 * - long 이 아니라 Long : 값이 안 오면 0이 아니라 null 이 되어 문제가 눈에 보임
 */